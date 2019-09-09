from moviepy.editor import VideoFileClip
from yolo_pipeline import *
from lane import *
import matplotlib.pyplot as plt
import csv
import ast
import numpy as np
import os
from prettytable import PrettyTable
from scipy.optimize import curve_fit


f = open('time.txt',"r+")
f.truncate()


def pipeline_yolo(img):

    img_undist, img_lane_augmented, lane_info = lane_process(img)
    output = vehicle_detection_yolo(img_undist, img_lane_augmented, lane_info)

    return output


def test_func(x, a, b, c):
    return a * np.exp(-b*x) + c


if __name__ == "__main__":
    # YOLO Pipeline
    # video_output = 'examples/video_output/YOLO/0726test.mp4'
    # clip1 = VideoFileClip("examples/video_input/output_4.mp4").subclip(0,5)
    path_input = r'examples/carla_input'
    video_name = 0
    velocity_name = 0
    position_name = 0
    fig_name = 0
    for root, dirs, files in os.walk(path_input):
        files.sort()
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filepath = os.path.join(root, file)
                print('Input File:',filepath)
                clip1 = VideoFileClip(filepath).subclip(0,5)
                clip = clip1.fl_image(pipeline_yolo)
                video_name = video_name + 1
                video_output = 'examples/carla_output/'+str(video_name)+'.mp4'
                clip.write_videofile(video_output, audio=False)
                print('\n')
                xx = []
                yy = []
                yys = []
                zz = []
                for line in open('velocity.txt','r'):
                    values = [float(s) for s in line.split()]
                    yy.append(values[0])
                for line in open('yy.txt','r'):
                    value = [float(s) for s in line.split()]
                    zz.append(value[0])
                xx = np.arange(1,len(yy)+1,1)
                frame_rate = 1/30
                xx = xx * frame_rate
                for i in range(len(xx)):
                    xx[i]='%.2f'%xx[i]
                    f = open("time.txt","a+")
                    f.write(str(xx[i])+"\n")
                
                ############################### output csv file
                speed = []
                time = []
                position = []
                fd = open("velocity.txt","r")
                for line in fd.readlines():
                    speed.append(list(map(float,line.split(','))))
                fd.close
                fd = open("yy.txt","r")
                for line in fd.readlines():
                    position.append(list(map(float,line.split(','))))
                fd.close
                fd = open("time.txt","r")
                for line in fd.readlines():
                    time.append(list(map(float,line.split(','))))
                if len(time) != len(speed):
                    time.append(list([5.00]))
                speed_array = np.array(speed)
                position_array = np.array(position)
                time_array = np.array(time)
                time_speed = np.hstack((time_array,speed_array))
                time_position = np.hstack((time_array,position_array))
                velocity_name = velocity_name + 1
                velocity_output = "examples/carla_csv/velocity"+str(velocity_name)+".csv"
                # with open("examples/carla_csv/velocity.csv","w") as csvfile:
                with open(velocity_output,"w") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Time","Velocity"])
                    writer.writerows(time_speed)
                position_name = position_name + 1
                position_output = "examples/carla_csv/position"+str(position_name)+".csv"
                # with open("examples/carla_csv/position.csv","w") as csvfile:
                with open(position_output,"w") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Time","Position"])
                    writer.writerows(time_position)
                ##############################

                ############################## plots #####################
                true_velocity = 'examples/carla_true_v/'+str(os.path.splitext(os.path.basename(filepath))[0])+'.txt'
                # print(true_velocity)
                lnum = 0
                with open(true_velocity,'r') as f:
                    for line in f:
                        lnum += 1
                        if (lnum >= 0) & (lnum <= 150):
                            yys.append(float(line))
                xxs = np.arange(1,len(yys)+1,1)
                xxs = xxs * frame_rate

                ############# print table ##############
                # table = PrettyTable(['Time (s)','Velocity (m/s)','Position (m)'])
                # for i in range(len(xx)):
                #     table.add_row([xx[i], yy[i], zz[i]])
                # print(table)
                ########################################

                ############ velocity ##############
                velocity_fig = "examples/carla_fig/velocity"+str(velocity_name)+".jpg"
                fig_name = fig_name + 1
                plt.figure(fig_name)
                plt.figure(figsize=(16,9))
                plt.xlabel("Time (s)")
                plt.ylabel("Velocity (m/s)")
                plt.plot(xx, yy, color="r", linewidth=1.5, label='Detected')
                plt.plot(xxs, yys, color="b", linewidth=1.5, label='True') ## true velocity
                yy = np.array(yy)
                
                ####################### curve fit ##########################
                # if len(yy) != len(xx):
                #     xx.append(5.0)
                # f1 = np.polyfit(xx,yy,3)
                # p1 = np.poly1d(f1)
                # yvals = p1(xx)
                # # popt, pcov = curve_fit(test_func, xx, yy)
                # # yvals = [test_func(i, popt[0], popt[1], popt[2]) for i in xx]
                # plt.plot(xx,yvals, color="g", linewidth=1.5, label='curve fit')
                # # params, params_covariance = curve_fit(test_func, xx, yy)
                # # plt.plot(xx,yy, color="g", linewidth=1.5, label='curve fit')
                ###############################################################

                plt.legend(loc='upper right')
                plt.title("Velocity vs Time (Detection box)")
                plt.savefig(velocity_fig)
                plt.close()
                #plt.title("Velocity vs Time (Lane)")

                ############ position #############
                position_fig = "examples/carla_fig/position"+str(position_name)+".jpg"
                fig_name = fig_name + 1
                plt.figure(fig_name)
                plt.figure(figsize=(16,9))
                plt.xlabel("Time (s)")
                plt.ylabel("Position (m)")
                plt.plot(xx, zz, color = "r", linewidth=1.5)
                plt.title("Position vs Time ")
                plt.savefig(position_fig)
                plt.close()
                f = open('velocity.txt',"r+")
                f.truncate()
                f = open('yy.txt',"r+")
                f.truncate()
                f = open('time.txt',"r+")
                f.truncate()
                #################################################