import tkinter as tk
import cv2


def CreateDict():
    dict = {}
    f = open('dnn_model/classes.txt', 'r')
    ct = 0
    while True:
        line = f.readline()
        if not line:
            break
        else:
            dict[ct] = line.strip()
            ct = ct + 1
    return dict

def RetString(dict,id):
    return dict[id]

def show(event,writetxt):
    txt = writetxt.get()
    frames= Frames(txt)

class Frames():
    def __init__(self, txt):
        dict = CreateDict()
        print("text: ",txt)
        net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")  # model deja antrenat
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size = (320,320), scale = 1/255)
        capture = cv2.VideoCapture(0)
        while True:
            ret, frame = capture.read()

            (class_ids, scores, bboxes) = model.detect(frame)
            print("class_id: ",class_ids, "\nscore: ", scores , " boxes: " , bboxes ,"\n")

            for class_id, score, bbox in zip(class_ids, scores, bboxes):
                (x, y, w, h) = bbox
                if RetString(dict,class_id) == txt:
                    cv2.putText(frame,  txt, (x,y-10),cv2.FONT_HERSHEY_PLAIN,2, (200, 0, 50),2)
                    cv2.rectangle(frame,(x,y), (x+w, y+h), (200,0,50),2)

            cv2.imshow("Frame ", frame)
            cv2.waitKey(1)

class MainWindow():
    def __init__(self,name):
        window = tk.Tk()
        window.title(name)
        window.resizable(False, False)
        window.geometry('400x100')
        window['bg'] = 'red'
        buttonsFrame = tk.Frame(master=window, background= 'red')
        searchWord = tk.Button(master=buttonsFrame, text = "Search it!", width=13)
        writeResult = tk.Entry(master = buttonsFrame,  width=14)
        buttonsFrame.pack( padx = 10)
        searchWord.pack( padx = 10, pady = 10)
        writeResult.pack()
        searchWord.bind("<Button-1>", lambda event: show(event,writeResult))

        window.mainloop()
    
        
if __name__ == '__main__':     
    win = MainWindow("Image Recognition")
    
