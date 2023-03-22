from flask import Flask, render_template, request, redirect, url_for, flash, abort
from app import app, db
from models import Player, Result, PlayerRating
from slugify import slugify
from sqlalchemy import func, or_
import json

@app.route('/')
def index():
    players = Player.query.filter_by(is_active=True).order_by(Player.rating.desc(), Player.name.asc()).all()
    results = Result.query.order_by(Result.date_played.desc()).limit(10).all()
    latest_results = Result.query.order_by(Result.date_played.desc()).limit(1).all()

    latest_players = []
    for result in latest_results:
        latest_players.extend([result.player1, result.player2])

    return render_template('index.html', players=players, results=results, latest_players=latest_players)


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/spelare', methods=['GET'])
def get_players():
    players = Player.query.filter_by(is_active=True).order_by(Player.name).all()
    
    if request.headers.get('HX-Request') == 'true':
        return render_template('partials/_matchModal.html', players=players)
    else:
        return render_template('players.html', players=players)


@app.route('/spelare/<string:player_slug>')
def player_detail(player_slug):
    player = Player.query.filter_by(slug=player_slug).first()
    rating_history = PlayerRating.query.filter_by(player_id=player.id).order_by(PlayerRating.date_created.asc()).all()
    rating_history = [{'date_created': str(rating.date_created), 'rating': rating.rating} for rating in rating_history]

    if not player:
        abort(404)
    
    # Hämta vinstrapport som player1
    player1_results = Result.query.filter_by(player1_id=player.id).all()
    player1_wins = 0
    player1_losses = 0
    for result in player1_results:
        if result.winner_id == player.id:
            player1_wins += 1
        else:
            player1_losses += 1
    player1_wr = player1_wins / max((player1_wins + player1_losses), 1)
    
    # Hämta vinstrapport som player2
    player2_results = Result.query.filter_by(player2_id=player.id).all()
    player2_wins = 0
    player2_losses = 0
    for result in player2_results:
        if result.winner_id == player.id:
            player2_wins += 1
        else:
            player2_losses += 1
    player2_wr = player2_wins / max((player2_wins + player2_losses), 1)

    return render_template('player_detail.html', player=player, rating_history_json=json.dumps(rating_history), player1_wins=player1_wins, 
    player1_losses=player1_losses, player2_wins=player2_wins, player2_losses=player2_losses, player1_wr=player1_wr, player2_wr=player2_wr)


@app.route('/ny_spelare', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name = request.form['name'].strip()
        slug = slugify(name)
        
        if not name:
            flash('Namnet får inte vara blankt', 'danger')
            return redirect(url_for('add_player'))
        
        if len(name) > 20:
            flash('Namn får inte vara längre än 20 tecken', 'danger')
            return redirect(url_for('add_player'))
        
        if Player.query.filter(func.lower(Player.name) == func.lower(name)).first():
            flash('Namnet finns redan', 'danger')
            return redirect(url_for('add_player'))
        
        player = Player(name=name, slug=slug)
        db.session.add(player)
        db.session.commit()
        flash(f'{player.name} har lagts till.', 'success')
        return redirect(url_for('index'))
    
    elif request.headers.get('HX-Request') == 'true':
        return render_template('partials/_addplayerModal.html')
    
    else:
        return redirect(url_for('index'))


@app.route('/spelare/<string:player_slug>/inaktivera', methods=['POST'])
def deactivate_player(player_slug):
    player = Player.query.filter_by(slug=player_slug).first()
    if player:
        player.is_active = False
        db.session.commit()
        flash(f'Spelaren {player.name} har inaktiverats', 'danger')
        return redirect(url_for('index'))
    else:
        flash('Ogilitig spelare', 'danger')
        return redirect(url_for('index'))


@app.route('/resultat', methods=['GET'])
def get_results():
    results = Result.query.order_by(Result.date_played.desc()).all()

    windowside_wins = 0
    wallside_wins = 0
    total_matches = len(results)

    if results:
        for result in results:
            if result.winner == result.player1:
                windowside_wins += 1
            elif result.winner == result.player2:
                wallside_wins += 1

        windowside_wins = round((windowside_wins / total_matches) * 100, 2)
        wallside_wins = round((wallside_wins / total_matches) * 100, 2)

    return render_template('results.html', results=results, windowside_wins=windowside_wins, wallside_wins=wallside_wins)


@app.route('/delete_result/<int:result_id>', methods=['POST'])
def delete_result(result_id):
    result = Result.query.get(result_id)
    if result:
        player1 = result.player1
        player2 = result.player2
        if result.winner == player1:
            player1.wins -= 1
            player2.losses -= 1
        elif result.winner == player2:
            player2.wins -= 1
            player1.losses -= 1
        db.session.delete(result)
        db.session.commit()
        flash('Matchen raderad', 'danger')
    return redirect(url_for('index'))


@app.route('/reset', methods=['POST'])
def reset_results():
    PlayerRating.query.delete()
    Result.query.delete()

    db.session.query(Player).update({
        Player.wins: 0,
        Player.losses: 0,
        Player.rating: 1000,
        Player.latest_rating_change: 0
    })

    db.session.query(Player).filter(Player.is_active==False).delete()
    
    db.session.commit()
    flash('Alla resultat och alla spelares statistik har nollställts', 'danger')
    return redirect(url_for('index'))


@app.route('/add_result', methods=['POST'])
def save_result():

    # Valideringar
    player1 = Player.query.filter_by(id=request.form['player1']).first()
    player2 = Player.query.filter_by(id=request.form['player2']).first()

    if not player1 or not player2:
        flash('Båda spelarna måste fyllas i', 'danger')
        return redirect(url_for('index'))

    player1_score = request.form['player1_score']
    player2_score = request.form['player2_score']

    if player1_score == '':
        player1_score = None
    else:
        player1_score = int(player1_score)

    if player2_score == '':
        player2_score = None
    else:
        player2_score = int(player2_score)

    if player1_score is None or player2_score is None:
        flash('Poängen för båda spelarna måste fyllas i', 'danger')
        return redirect(url_for('index'))

    if player1_score == player2_score:
        flash('Matchen kan inte sluta oavgjort', 'danger')
        return redirect(url_for('index'))

    if player1 == player2:
        flash('En spelare kan inte möta sig själv', 'danger')
        return redirect(url_for('index'))

    # Hämta antalet spelade matcher för båda spelarna för K_FACTOR
    num_games_player1 = player1.num_games()
    num_games_player2 = player2.num_games()

    if num_games_player1 < 20:
        K_FACTOR_PLAYER1 = 24
    elif num_games_player1 < 50:
        K_FACTOR_PLAYER1 = 18
    elif num_games_player1 < 100:
        K_FACTOR_PLAYER1 = 12
    else:
        K_FACTOR_PLAYER1 = 8

    if num_games_player2 < 20:
        K_FACTOR_PLAYER2 = 24
    elif num_games_player2 < 50:
        K_FACTOR_PLAYER2 = 18
    elif num_games_player2 < 100:
        K_FACTOR_PLAYER2 = 12
    else:
        K_FACTOR_PLAYER2 = 8

    # Beräkna förväntat resultat för spelarna
    player1_expected = 1 / (1 + 10 ** ((player2.rating - player1.rating) / 400))
    player2_expected = 1 - player1_expected

    # Bestäm vinnaren och beräkna poängskillnaden
    if player1_score > player2_score:
        player1_result = 1
        player2_result = 0
        score_diff = player1_score - player2_score
    elif player2_score > player1_score:
        player1_result = 0
        player2_result = 1
        score_diff = player2_score - player1_score

    # Hämta ratingskillnaden och använd som värde för beräkning av expected_score
    rating_diff = player2.rating - player1.rating
    expected_score = 1 / (1 + 10 ** (rating_diff / 400))

    # Beräkna min_rating_change utefter expected_score ovan
    min_rating_change = 24 * (1 - expected_score)

    # Faktor för att justera rating beroende på antal poäng i matchen
    score_factor = max(1, (score_diff / 2 + 3) / 4)

    # Beräkna ratingförändringen för båda spelarna
    player1_rating_change = round(K_FACTOR_PLAYER1 * (player1_result - player1_expected - min_rating_change / 800) * score_factor)
    player2_rating_change = round(K_FACTOR_PLAYER2 * (player2_result - player2_expected - min_rating_change / 800) * score_factor)

    player1.rating += player1_rating_change
    player2.rating += player2_rating_change

    # Sätt minimumrating till 100 för att undvika att en spelare går ner till minus
    if player1.rating < 100:
        player1.rating = 100
    if player2.rating < 100:
        player2.rating = 100

    # Uppdatera parametrar att skriva till databasen
    player1.latest_rating_change = player1_rating_change
    player2.latest_rating_change = player2_rating_change

    if player1_score > player2_score:
        player1.wins += 1
        player2.losses += 1
        winner = player1
    elif player2_score > player1_score:
        player2.wins += 1
        player1.losses += 1
        winner = player2

    new_result = Result(player1=player1, player2=player2, player1_score=player1_score, player2_score=player2_score, winner=winner)

    # Spara ratinghistoriken för att användas i diagram
    db.session.add(PlayerRating(player=player1, rating=player1.rating))
    db.session.add(PlayerRating(player=player2, rating=player2.rating))

    db.session.add(new_result)
    db.session.commit()

    flash('Matchen registrerad', 'success')
    return redirect(url_for('index'))