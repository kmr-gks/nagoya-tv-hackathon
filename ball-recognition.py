#https://temari.co.jp/blog/2021/01/10/opencv-13/
'''
動作環境
HP Pavilion 15
Windows 11 Home 23H2
intelcpu, iris xe graphics
Python 3.11.9
opencv-python 4.10.0
'''
import cv2
import numpy as np
cap=cv2.VideoCapture(0) #カメラから入力

cv2.namedWindow('video', cv2.WINDOW_NORMAL)

#マスク画像取得
def getMask(l, u):
    # 動画を最後まで再生すると終了
    if frame is None: exit()

    # HSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array(l)
    upper = np.array(u)
    if lower[0] >= 0:
        #色相が正の値のとき、赤以外のマスク
        mask = cv2.inRange(hsv, lower, upper)
    else:
        #色相が負の値のとき、赤用マスク
        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]
        mask = np.zeros(h.shape, dtype=np.uint8)
        mask[((h < lower[0]*-1) | h > upper[0]) & (s > lower[1]) & (s < upper[1]) & (v > lower[2]) & (v < upper[2])] = 255

    return cv2.bitwise_and(frame,frame, mask= mask)

# 輪郭取得
def getContours(img,t,r):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)

    #cv2.findContours の戻り値がOpenCVのバージョンによって異なる
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #タプルをリストに変換する必要がある
    contours=list(contours)
    #初期化
    radius_frame = frame

    # 一番大きい輪郭を抽出
    contours.sort(key=cv2.contourArea, reverse=True)

    #一つ以上検出
    if len(contours) > 0:
        for cnt in contours:
            # 最小外接円を描く
            (x,y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            
            if radius > r:
                radius_frame = cv2.circle(frame,center,radius,(0,255,0),10)
                #座標をウィンドウに表示
                cv2.putText(frame, str(center), [10,50], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        return radius_frame
    else:
        return frame


while(1):
    _, frame = cap.read()

    # ウィンドウのサイズを取得
    _, _, win_width, win_height = cv2.getWindowImageRect('video')


    # マスクの最小HSVと最大HSVを指定　ただし赤の場合は最小Hを負の値にする（独自ルール）
    # 青マスク H110～150、S45～255、V100～255
    #res_blue = getMask([110,45,100], [150,255,255])

    # 赤マスク H0～10または170～180、S50～255、V200～255
    res_red = getMask([-10,50,200], [170,255,255])

    #輪郭取得
    contours_frame = getContours(res_red, 50, 30) # (画像, 明度閾値, 最小半径)

    # フレームの縦横比を取得
    h, w, _ = frame.shape
    aspect_ratio = w / h

    # ウィンドウの縦横比を計算
    if win_width / win_height > aspect_ratio:
        # ウィンドウが横長の場合
        new_height = win_height
        new_width = int(aspect_ratio * new_height)
    else:
        # ウィンドウが縦長の場合
        new_width = win_width
        new_height = int(new_width / aspect_ratio)

    # フレームを新しいサイズにリサイズ
    resized_frame = cv2.resize(contours_frame, (new_width, new_height))

    # 黒い背景を作成して、リサイズしたフレームを中央に配置
    black_background = np.zeros((win_height, win_width, 3), dtype=np.uint8)
    start_x = (win_width - new_width) // 2
    start_y = (win_height - new_height) // 2

    # リサイズしたフレームを黒い背景に配置
    black_background[start_y:start_y + new_height, start_x:start_x + new_width] = resized_frame

    # 表示
    cv2.imshow('video',black_background)

    k = cv2.waitKey(25) & 0xFF
    #Q で終了
    if k == ord('q'):
        break
    # ウィンドウのxボタンで終了
    try:
        if cv2.getWindowProperty('video', cv2.WND_PROP_AUTOSIZE) < 0:
            break
    except:
        break

cap.release()
cv2.destroyAllWindows()