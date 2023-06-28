import chess
import chess.engine

def sf_calc(fen, check):
    stockfish = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/stockfish/15.1/bin/stockfish")
    leela = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/lc0/0.29.0/bin/lc0")
    
    # stockfish = chess.engine.SimpleEngine.popen_uci("/home/jfernandes33/packages/stockfish/15.1/bin/stockfish")
    # leela = chess.engine.SimpleEngine.popen_uci("/home/jfernandes33/packages/lc0/0.29.0/bin/lc0")
    board = chess.Board()
    board.set_fen(fen)
    response = stockfish.analyse(board, chess.engine.Limit(time=.1))

    result = stockfish.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)

    sf = stockfish.analyse(board, chess.engine.Limit(time=.1))
    lc0 = leela.analyse(board, chess.engine.Limit(time=.1))



    if (check and (lc0["pv"][0] not in sf["pv"][0:3])):
        next_move  = chess.Move.uci(lc0["pv"][0])
    else:
        next_move = None
    cp = sf['score'].relative.cp
    stockfish.quit()
    leela.quit()
    return chess.Move.uci(response['pv'][0]), next_move, cp
