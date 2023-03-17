from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db
from models import Player, Result, PlayerRating

@app.route('/')
def index():
    players = Player.query.order_by(Player.rating.desc()).all()
    results = Result.query.order_by(Result.date_played.desc()).limit(10).all()
    return render_template('index.html', players=players, results=results)


@app.route('/get_players', methods=['GET'])
def get_players():
    players = Player.query.filter_by(is_active=True).order_by(Player.name).all()
    return render_template('partials/_matchModal.html', players=players)


@app.route('/result', methods=['POST'])
def save_result():

    # Validations
    player1 = Player.query.filter_by(id=request.form['player1']).first()
    player2 = Player.query.filter_by(id=request.form['player2']).first()

    if not player1 or not player2:
        flash('Båda spelarna måste fyllas i')
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
        flash('Poängen för båda spelarna måste fyllas i')
        return redirect(url_for('index'))

    if player1_score == player2_score:
        flash('Matchen kan inte sluta oavgjort')
        return redirect(url_for('index'))

    if player1 == player2:
        flash('En spelare kan inte möta sig själv')
        return redirect(url_for('index'))

    # Get number of games for each player for K_FACTOR
    num_games_player1 = player1.num_games()
    num_games_player2 = player2.num_games()

    if num_games_player1 < 20:
        K_FACTOR_PLAYER1 = 32
    elif num_games_player1 < 50:
        K_FACTOR_PLAYER1 = 24
    elif num_games_player1 < 100:
        K_FACTOR_PLAYER1 = 16
    else:
        K_FACTOR_PLAYER1 = 8

    if num_games_player2 < 20:
        K_FACTOR_PLAYER2 = 32
    elif num_games_player2 < 50:
        K_FACTOR_PLAYER2 = 24
    elif num_games_player2 < 100:
        K_FACTOR_PLAYER2 = 16
    else:
        K_FACTOR_PLAYER2 = 8

    # Calculate expected scores
    player1_expected = 1 / (1 + 10 ** ((player2.rating - player1.rating) / 400))
    player2_expected = 1 - player1_expected

    # Calculate new ratings
    if player1_score > player2_score:
        player1_result = 1
        player2_result = 0
        score_diff = player1_score - player2_score
    elif player2_score > player1_score:
        player1_result = 0
        player2_result = 1
        score_diff = player2_score - player1_score

    # Calculate rating changes
    rating_diff = player2.rating - player1.rating
    expected_score = 1 / (1 + 10 ** (rating_diff / 400))

    # Calculate the minimum amount of rating points the lower rated player should gain
    min_rating_change = 16 * (1 - expected_score)

    # The factor for adjusting rating depending on score
    score_factor = max(1, (score_diff / 2 + 3) / 4)

    # Calculate rating changes
    player1_rating_change = round(K_FACTOR_PLAYER1 * (player1_result - expected_score - min_rating_change / 800) * score_factor)
    player2_rating_change = round(K_FACTOR_PLAYER2 * (player2_result - (1 - expected_score) - min_rating_change / 800) * score_factor)

    player1.rating += player1_rating_change
    player2.rating += player2_rating_change

    # Set minimum rating to 100
    if player1.rating < 100:
        player1.rating = 100
    if player2.rating < 100:
        player2.rating = 100

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

    # Save the rating for history
    db.session.add(PlayerRating(player=player1, rating=player1.rating))
    db.session.add(PlayerRating(player=player2, rating=player2.rating))

    db.session.add(new_result)
    db.session.commit()

    return redirect(url_for('index'))