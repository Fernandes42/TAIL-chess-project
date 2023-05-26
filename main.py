import chess
import chess.engine

# stockfish = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/stockfish/15.1/bin/stockfish")
# leela = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/lc0/0.29.0/bin/lc0")


# board = chess.Board()




# while not board.is_game_over():
#     result = stockfish.play(board, chess.engine.Limit(time=0.1))
#     board.push(result.move)
#     # display(board)
#     print(board)
#     if game_type == 1:
#         sf = stockfish.analyse(board, chess.engine.Limit(time=1))
#         lc0 = leela.analyse(board, chess.engine.Limit(time=1))
#     user_move = input("Enter your move:  ")
#     try:
#         board.push_san(user_move)
#     except:
#         break
#     if game_type == 1:
#         if lc0["pv"][0] not in sf["pv"]:
#             print(lc0["pv"][0])

def sf_calc(fen):
    stockfish = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/stockfish/15.1/bin/stockfish")
    board = chess.Board()
    board.set_fen(fen)
    # board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
    sf = stockfish.analyse(board, chess.engine.Limit(time=.1))
    stockfish.quit()

    return chess.Move.uci(sf['pv'][0])
# stockfish.quit()
# leela.quit()