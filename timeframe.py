#!/usr/bin/python
import datetime

TIME_FRAME_START_DAY = 7 #Sunday
TIME_FRAME_START_HOUR = 4 # 4am
TIME_FRAME_DAYS = 7


def get_time_frames(period_init: datetime.datetime, period_end: datetime.datetime):

    #explicit datetime conversion
    period_init = datetime.datetime(period_init.year, period_init.month, period_init.day)
    period_end = datetime.datetime(period_end.year, period_end.month, period_end.day)

    # initialize first frame limits
    frame_duration = datetime.timedelta(TIME_FRAME_DAYS)
    init_delta = datetime.timedelta(period_init.isoweekday() % TIME_FRAME_START_DAY)

    # define first frame
    frame_start = datetime.datetime.combine((period_init - init_delta), datetime.time(hour=4))
    last_frame_end = frame_start + frame_duration

    frames = []

    while last_frame_end < period_end:

        #print(frame_start, last_frame_end)
        frames.append([frame_start, last_frame_end])
        frame_start = last_frame_end
        last_frame_end = frame_start + frame_duration

    return frames
