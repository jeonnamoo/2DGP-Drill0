from pico2d import open_canvas, close_canvas
import game_framework
import play_mode as start_mode

open_canvas(1600, 600)  # 캔버스 크기를 설정
game_framework.run(start_mode)  # start_mode로 시작
close_canvas()
