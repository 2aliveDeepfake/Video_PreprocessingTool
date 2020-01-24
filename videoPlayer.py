import math
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import cv2
import time
from tkinter import ttk
import os


#######################################################################################################
#★★★★먼저 tkinter를 설치해주시기 바랍니다.★★★★
#conda: conda install -c anaconda tk
#기존 영상이 너무 커서 원하는 만큼 영상의 가로/세로 길이를 정해줍니다.
#영상에서 뽑을 이미지를 저장하는 경로를 설정합니다.
#경로에 한글이 있으면 저장이 되지 않을 수도 있으니 저장이 되는지 먼저 확인해주시기 바랍니다.
#######################################################################################################

width = 400
height = 300
path = "C:/Users/jsych/Desktop/Results/"

class videoPlayer:
    def __init__(self, window, window_title):

        #비디오를 표시해 줄 윈도우를 만든다.
        #윈도우이름은 window_title이다.
        self.window = window
        self.window.title(window_title)

        #윈도우 창 안에서 영역을 나눠준다.
        #여기서는 위와 아래 부분으로 영역을 나눈다.
        #top_frame은 영상, middle_frame은 트랙바, bottom_frame은 버튼이 위치한다.
        #side가 같으면 먼저 생성된 frame부터 쌓인다.
        top_frame = Frame(self.window)
        top_frame.pack(side=TOP, pady=5)

        middle_frame = Frame(self.window)
        middle_frame.pack(side=TOP, pady=5)

        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=TOP, pady=20)

        bottom_frame2 = Frame(self.window)
        bottom_frame2.pack(side=TOP, pady=20)

        left_frame = Frame(self.window)
        left_frame.pack(side=LEFT, pady=5)

        right_frame = Frame(self.window)
        right_frame.pack(side=RIGHT, pady=5)

        #일시정지 여부 파라미터
        self.pause = False

        #영상을 보여주기 위해 top_frame에 Canvas를 배치한다. 배경은 검정색으로 한다.
        self.canvas = Canvas(top_frame, width=width, height=height, bg="black")
        self.canvas.pack()

        #영상 트랙바
        #트랙바는 Canvas의 가로 길이와 같고, 수평바로 한다.
        self.trackbar = Scale(middle_frame, length=self.canvas.winfo_reqwidth(), orient=HORIZONTAL)
        self.trackbar.pack(side=LEFT, anchor=CENTER)

        #영상의 남은 시간
        #남은 시간은 트랙바 옆에 생성한다.
        self.showTime = Label(middle_frame, text=time.strftime('%M:%S', time.gmtime(0)))
        self.showTime.pack(side=RIGHT, anchor=CENTER)

        #영상좌우넘기기버튼
        self.btn_leftframe = Button(middle_frame, text="◀", width=5, command=self.to_leftframe)
        # self.btn_leftframe.bind('<Button-1>', self.ButtonState)
        self.btn_rightframe = Button(middle_frame, text="▶", width=5, command=self.to_rightframe)
        self.btn_leftframe.pack(side=LEFT, anchor=CENTER)
        self.btn_rightframe.pack(side=LEFT, anchor=CENTER)


        #영상불러오기 버튼
        self.btn_select=Button(bottom_frame, text="영상불러오기", width=15, command=self.open_file)
        self.btn_select.grid(row=1, column=0)

        #재생버튼
        self.btn_play=Button(bottom_frame, text="재생", width=15, command=self.start_video)
        self.btn_play.grid(row=1, column=1)

        #정지버튼
        self.btn_pause=Button(bottom_frame, text="일시정지", width=15, command=self.pause_video)
        self.btn_pause.grid(row=1, column=2)

        #영상 편집 버튼
        self.postTimeLabel = Label(bottom_frame2, text="여기부터: ")
        self.postTimeLabel.grid(row=0, column=0)
        self.inputpostTimestr = StringVar()
        self.inputpostTimebox = ttk.Entry(bottom_frame2, width=5, textvariable=self.inputpostTimestr)
        self.inputpostTimebox.grid(row=0, column=1)
        
        self.secondstr = Label(bottom_frame2, text="초 ~ ")
        self.secondstr.grid(row=0, column=2)

        self.nextTimeLabel = Label(bottom_frame2, text="여기까지: ")
        self.nextTimeLabel.grid(row=0, column=3)
        self.inputnextTimestr = StringVar()
        self.inputnextTimebox = ttk.Entry(bottom_frame2, width=5, textvariable=self.inputnextTimestr)
        self.inputnextTimebox.grid(row=0, column=4)

        self.secondstr = Label(bottom_frame2, text="초")
        self.secondstr.grid(row=0, column=5)

        self.fpsLabel = Label(bottom_frame2, text="fps: ")
        self.fpsLabel.grid(row=0, column=6)

        self.inputfpsstr = StringVar()
        self.inputfpsbox = ttk.Entry(bottom_frame2, width=5, textvariable=self.inputfpsstr)
        self.inputfpsbox.grid(row=0, column=7)

        # self.cutVideo_btn = Button(bottom_frame2, text="편집하기", width=10, command=self.cut_video)
        # self.cutVideo_btn.grid(row=0, column=

        #현재 프레임 저장버튼
        self.nowframe_savebtn = Button(left_frame, text="현재프레임저장", width=20, command=self.nowframe_save)
        self.nowframe_savebtn.pack(anchor=CENTER, fill="both")

        #구간 저장버튼
        self.section_savebtn = Button(right_frame, text="지정구간저장", width=20, command=self.section_save)
        self.section_savebtn.pack(anchor=CENTER, fill="both")


        self.delay = 15   # ms

        self.window.mainloop()


    def open_file(self):

        self.pause = True

        self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("MP4 files", "*.mp4"), ("WMV files", "*.wmv"), ("AVI files", "*.avi")))
        self.Filename = self.filename
        self.Filename = self.Filename.split("/")[-1]
        self.Filename = self.Filename.split(".")[0]
        print(self.filename)
        # print(Filename)

        # Open the video file
        self.cap = cv2.VideoCapture(self.filename)

        #불러온 영상의 가로, 세로길이, 총프레임, 초당프레임, 재생시간(총프레임/초당프레임)을 구한다.
        # self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.time_total = math.floor(self.frame / self.fps)
        self.nowframe = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.time_remain = math.floor((self.frame - self.nowframe) / self.fps)

        # print(self.frame)
        print(self.fps)

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.nowframe)
        ret, frame = self.get_frame()

        #Canvas랑 Trackbar의 길이를 지정한 가로길이에 맞춰준다.
        #영상의 시간도 가져와서 표시한다.
        self.canvas.config(width=width, height=height)
        self.trackbar.config(length=width, from_=0, to=self.frame)
        self.trackbar.set(0)
        self.showTime.config(text=time.strftime('%M:%S', time.gmtime(self.time_remain)))

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

    #비디오를 frame 마다 가져오는 부분
    def get_frame(self):
        try:
            if self.cap.isOpened():
                #만약 비디오를 읽었으면 ret는 True를, frame은 이미지를 return한다.
                ret, frame = self.cap.read()
                frame = cv2.resize(frame, dsize=(width, height), interpolation=cv2.INTER_AREA)
                # return (ret, frame)
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        except:
            messagebox.showerror(title='Video file not found', message='Please select a video file.')


    def play_video(self):
        #비디오에서 이미지를 가지고 오고, 리사이즈를 한다(이미지가 너무 크면 아래 버튼이 안보임).
        ret, frame = self.get_frame()
        #print(self.trackbar.get())
        #일시정지 후, 다시 영상을 시작하려면 정지한 구간의 값이 필요하다.
        if self.pause:
            self.window.after_cancel(self.after_id)

        else:
            # 플레이 상태면 array인 frame을 PIL에서 이미지로 바꾸고 Canvas에 넣어준다.
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.itemconfig(self.image_on_canvas, image = self.photo)

            #현재frame의 값을 가져온다.
            self.nowframe = self.cap.get(cv2.CAP_PROP_POS_FRAMES)

            #전체frame에서 현재frame 값을 빼준 뒤, 초당 frame으로 나눠주면 남은 시간이 된다.
            self.time_remain = math.floor((self.frame - self.nowframe) / self.fps)

            #남은 시간을 보여준다
            self.showTime.config(text=time.strftime('%M:%S', time.gmtime(self.time_remain)))

            #트랙바에 현재 frame 갱신해준다.
            self.trackbar.set(self.nowframe + 1)

            #정지한 구간을 얻기위해 일정 딜레이(ms)이후 비디오가 플레이된 시간을 계산한다.
            self.after_id = self.window.after(self.delay, self.play_video)

    #btn_play버튼에 들어가는 함수로 일시정지 상태면 False로 바꿔주고, 영상의 시작시간을 트랙바가 위치한 시간으로 바꿔준다.
    #이후 영상을 재생한다.
    def start_video(self):
        #일시정지 상태일때만 실행
        if(self.pause):
            self.pause = False
            self.cap.set(int(cv2.CAP_PROP_POS_FRAMES), self.trackbar.get())
            self.play_video()


    #btn_pause버튼에 들어가는 함수로 일시정지 상태를 True로 바꿔준다.
    def pause_video(self):
        self.pause = True

    #현재 frame 저장
    #폴더가 없을 경우 영상 이름으로 폴더를 만들고 그 폴더 안에 저장한다.
    def nowframe_save(self):
        print(self.Filename)
        try:
            if not (os.path.isdir(path + self.Filename)):
                os.makedirs(path + self.Filename)

        except OSError as e:
            if e.errno != e.errno.EEXIST:
                print("Failed to create directory!!!!!")
                raise
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.trackbar.get())
        ret, frame = self.cap.read()
        filename = path + self.Filename + "/" + self.Filename + "(" + str(self.trackbar.get()) + ")" + ".jpg"
        cv2.imwrite(filename, frame)
    
    #구간 저장
    #폴더가 없을 경우 영상 이름으로 폴더를 만들고 그 폴더 안에 저장한다.
    def section_save(self):
        try:
            if not (os.path.isdir(path + self.Filename)):
                os.makedirs(os.path.join(path + self.Filename))

        except OSError as e:
            if e.errno != e.errno.EEXIST:
                print("Failed to create directory!!!!!")
                raise

        # 영상이 재생되고 있을 수도 있어서 영상을 정지해준다.
        if not self.pause:
            self.pause_video()
        # print(self.inputpostTimestr.get())
        # print(self.inputnextTimestr.get())
        # print(self.inputfpsstr.get())

        success, image = self.cap.read()
        success = True

        # 현재frame은 트랙바값으로 한다.
        nowFrame = self.trackbar.get()
        # 현재Frame에서 앞으로 몇초, 뒤로 몇초를 잘라야한다.
        # 입력한 값을 가져오고, 현재 frame에서 입력한 값과 영상의 초당 프레임을 곱한 값(몇초 앞으로, 뒤로 갈지 값)을 빼준다.
        postFrame = nowFrame - (int(self.inputpostTimestr.get()) * self.fps)
        nextFrame = nowFrame + (int(self.inputnextTimestr.get()) * self.fps)

        # print("nowframe: " + str(nowFrame))
        # print("postTimer: " + str(int(self.inputpostTimestr.get())))
        # print("fps: " + str(self.fps))
        # print("postframe: " + str(postFrame))

        # 위의 값이 0보다 작거나 영상 길이보다 길면 맞춰준다.
        if (postFrame < 0):
            postFrame = 0
        if (nextFrame > self.frame):
            nextFrame = self.frame

        # 저장하는 코드
        #초당 몇 frame으로 할지 값을 정한다.
        frame_rate = int(self.inputfpsstr.get())

        #count변수는 현재frame에서 몇초 이전을 간 값을 맞춰준다.
        count = postFrame
        # print("post:" + str(postFrame))

        #체크 할 frame 가져오기
        n_frame = 0
        #영상의 끝까지 반복한다.
        while count <= nextFrame:
            print(count)
            #영상프레임을 count에 입력한 값으로 이동한다.
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            # print(count)
            #count가 이전프레임과 다음 프레임 사이까지 그리고 count를 전체frame으로 나눠준 나머지가 초당 몇 frame으로 한 값보다 작을때 이미지를 저장한다.
            if(postFrame <= count <= nextFrame and int(n_frame%self.fps)<frame_rate):
                filename = path + self.Filename + "/" + self.Filename + "(" + str(count) + ")" + ".jpg"
                cv2.imwrite(filename, image)
            #목표까지 계속 더한다
            count += 1
            n_frame += 1

        #끝나면 알림
        messagebox.showinfo(title='알림', message='저장이 완료 되었습니다.')

    def ButtonState(self, event):
        print("Clicked!!!")

    def to_leftframe(self):
        leftlocation = self.trackbar.get() - 1
        if leftlocation < 0:
            leftlocation = 0
        self.trackbar.set(leftlocation)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, leftlocation)
        ret, frame = self.get_frame()
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo)

        # 현재frame의 값을 가져온다.
        self.nowframe = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        # 전체frame에서 현재frame 값을 빼준 뒤, 초당 frame으로 나눠주면 남은 시간이 된다.
        self.time_remain = math.floor((self.frame - self.nowframe) / self.fps)
        # 남은 시간을 보여준다
        self.showTime.config(text=time.strftime('%M:%S', time.gmtime(self.time_remain)))


    def to_rightframe(self):
        rightlocation = self.trackbar.get() + 1
        if rightlocation > self.frame:
            rightlocation = self.frame
        self.trackbar.set(rightlocation)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, rightlocation)
        ret, frame = self.get_frame()
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo)

        # 현재frame의 값을 가져온다.
        self.nowframe = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        # 전체frame에서 현재frame 값을 빼준 뒤, 초당 frame으로 나눠주면 남은 시간이 된다.
        self.time_remain = math.floor((self.frame - self.nowframe) / self.fps)
        # 남은 시간을 보여준다
        self.showTime.config(text=time.strftime('%M:%S', time.gmtime(self.time_remain)))




    #편집하기
    def cut_video(self):
        #영상이 재생되고 있을 수도 있어서 영상을 정지해준다.
        if not self.pause:
            self.pause_video()
        # print(self.inputpostTimestr.get())
        # print(self.inputnextTimestr.get())
        # print(self.inputfpsstr.get())

        success, image = self.cap.read()
        success = True

        #현재frame은 트랙바값으로 한다.
        nowFrame = self.trackbar.get()
        #현재Frame에서 앞으로 몇초, 뒤로 몇초를 잘라야한다.
        #입력한 값을 가져오고, 현재 frame에서 입력한 값과 영상의 초당 프레임을 곱한 값(몇초 앞으로, 뒤로 갈지 값)을 빼준다.
        postFrame = nowFrame - (int(self.inputpostTimestr.get()) * self.fps)
        nextFrame = nowFrame + (int(self.inputnextTimestr.get()) * self.fps)

        # print("nowframe: " + str(nowFrame))
        # print("postTimer: " + str(int(self.inputpostTimestr.get())))
        # print("fps: " + str(self.fps))
        # print("postframe: " + str(postFrame))

        #위의 값이 0보다 작거나 영상 길이보다 길면 맞춰준다.
        if(postFrame < 0):
            postFrame = 0
        if(nextFrame > self.frame):
            nextFrame = self.frame


        #저장하는 코드
        # #초당 몇 frame으로 할지 값을 정한다.
        # frame_rate = int(self.inputfpsstr.get())
        #
        # #count변수는 현재frame에서 몇초 이전을 간 값을 맞춰준다.
        # count = postFrame
        # # print("post:" + str(postFrame))
        #
        # #체크 할 frame 가져오기
        # n_frame = 0
        # #영상의 끝까지 반복한다.
        # while count <= nextFrame:
        #     print(count)
        #     #영상프레임을 count에 입력한 값으로 이동한다.
        #     self.copyvideo.set(cv2.CAP_PROP_POS_FRAMES, count)
        #     # print(count)
        #     #count가 이전프레임과 다음 프레임 사이까지 그리고 count를 전체frame으로 나눠준 나머지가 초당 몇 frame으로 한 값보다 작을때 이미지를 저장한다.
        #     if(postFrame <= count <= nextFrame and int(n_frame%self.fps)<frame_rate):
        #         #한글경로 들어가면 안됨
        #         path = "C:/Users/jsych/Desktop/Results/"
        #         filename = path + "frame" + str(count) + ".jpg"
        #         cv2.imwrite(filename, image)
        #     #목표까지 계속 더한다
        #     count += 1
        #     n_frame += 1


        #미리보기창(계속해야함)
        # #Tk()는 한번만 부를 수 있어서 재사용하려면 Toplevel로 가져와야한다.
        # self.window2 = Toplevel(self.window)
        # self.window2.title("편집")
        #
        # cut_top_frame = Frame(self.window2)
        # cut_top_frame.pack(side=TOP, pady=5)
        #
        # cut_middle_frame = Frame(self.window2)
        # cut_middle_frame.pack(side=TOP, pady=5)
        #
        # #영상을 보여주기 위해 top_frame에 Canvas를 배치한다. 배경은 검정색으로 한다.
        # self.cut_canvas = Canvas(cut_top_frame, width=self.window2.winfo_reqwidth(), height=self.window2.winfo_reqheight(), bg="black")
        # self.cut_canvas.pack()
        #
        # #영상 트랙바
        # #트랙바는 Canvas의 가로 길이와 같고, 수평바로 한다.
        # self.cut_trackbar = Scale(cut_middle_frame, length=self.cut_canvas.winfo_reqwidth(), from_=postFrame, to=nextFrame, orient=HORIZONTAL)
        # self.cut_trackbar.set(nowFrame)
        # self.cut_trackbar.pack(side=LEFT, anchor=CENTER)
        #
        #
        # if self.cap.isOpened():
        #     self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cut_trackbar.get())
        #     read, cut_frame = self.cap.read()
        #     cv2.cvtColor(cut_frame, cv2.COLOR_RGB2GRAY)
        #     cut_frame = cv2.resize(cut_frame, dsize=(self.window2.winfo_reqwidth(), self.window2.winfo_reqheight()), interpolation=cv2.INTER_AREA)
        #     # 플레이 상태면 array인 frame을 PIL에서 이미지로 바꾸고 Canvas에 넣어준다.
        #     self.cut_photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cut_frame))
        #     self.cut_canvas.create_image(0, 0, image = self.cut_photo, anchor=NW)
        #
        #     # 현재frame의 값을 가져온다.
        #     self.cut_nowframe = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        #
        #     self.cut_trackbar.set(self.cut_nowframe + 1)





    #윈도우가 닫혔을때, 영상을 해제한다.
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

##### End Class #####


#비디오 플레이어 객체 생성
videoPlayer(Tk(), "영상편집")