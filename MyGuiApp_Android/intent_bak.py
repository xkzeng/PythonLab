# -*- coding: utf-8 -*-

#Name: Intent模块,实现消息机制;
#Desc: 应用于进程内部的消息处理机制,便于实现异步消息处理和简化应用程序编写;
#Create Time: ‎2018-08-20 20:00:00
#Author: zengxiankui
#Usage: 独立模块,导入即可;

import os, sys, time, signal, threading;
#reload(sys);
#sys.setdefaultencoding('utf8');

try:
    from queue import Queue as MessageQueue;
except Exception as e:
    from Queue import Queue as MessageQueue;

class Runnable:
    def __init__(self):
        pass;
    
    def __del__(self):
        pass;
    
    def execute(self, msg, result):
        pass;

#消息对象类:用于传递数据;
class Message:
    def __init__(self, _what, _id = -1, _target = None, _callback = None, _arg1 = 0, _arg2 = 0, _object = None):
        self.__id = _id < 0 and time.time() or _id;
        self.__what = _what;
        self.__target = _target;
        self.__callback = _callback; #Runnable
        self.__arg1 = _arg1;
        self.__arg2 = _arg2;
        self.__object = _object;
    
    def __del__(self):
        self.__id = 0;
        self.__what = 0;
        self.__target = None;
        self.__callback = None;
        self.__arg1 = 0;
        self.__arg2 = 0;
        self.__object = None;
        
    def get_id(self):
        return self.__id;
    
    def set_id(self, msgId):
        self.__id = msgId;
        
    def get_what(self):
        return self.__what;
    
    def set_what(self, what):
        self.__what = what;
        
    def get_target(self):
        return self.__target;
    
    def set_target(self, target):
        self.__target = target;
        
    def get_callback(self):
        return self.__callback;
    
    def set_callback(self, callback):
        self.__callback = callback;
        
    def get_arg1(self):
        return self.__arg1;
    
    def set_arg1(self, arg1):
        self.__arg1 = arg1;
        
    def get_arg2(self):
        return self.__arg2;
    
    def set_arg2(self, arg2):
        self.__arg2 = arg2;
        
    def get_object(self):
        return self.__object;
    
    def set_object(self, object):
        self.__object = object;

#消息循环线程:
class LopperThread(threading.Thread):
    def __init__(self, _looper):
        threading.Thread.__init__(self);
        self.name = "LooperThread";
        self.__looper = _looper;
        
    def __del__(self):
        pass;
    
    #重载的线程函数
    def run(self):
        print("线程" + self.getName() + "启动");
        self.__looper.prepare();
        self.__looper.loop();
        self.__looper.cleanup();
        print("线程" + self.getName() + "结束");

#消息循环类:
class Looper:
    def __init__(self):
        self.__running = True;
        self.__queue = MessageQueue();#消息队列;
        self.__lock = threading.Lock();
        pass;
    
    def __del__(self):
        pass;
    
    @staticmethod
    def get_looper():
        _looper = Looper();
        
        thrd = LopperThread(_looper);
        thrd.start();
        return _looper;
    
    def queue(self):
        return self.__queue;
    
    def is_running(self):
        self.__lock.acquire();
        flag = self.__running;
        self.__lock.release();
        return flag;
    
    def set_running_flag(self, flag):
        self.__lock.acquire();
        self.__running = flag;
        self.__lock.release();
        return 0;
    
    def quit(self):
        self.set_running_flag(False);
        return 0;
    
    def enqueue(self, msg):
        if(self.is_running()):
            self.__queue.put(msg);
            return True;
        else:
            print("this looper do not start");
            return False;
    
    def prepare(self):
        pass;
    
    def cleanup(self):
        pass;
    
    def loop_OLD(self):
        self.set_running_flag(True);
        
        while(self.is_running()):
            msg = self.__queue.get();
            target = msg.get_target();
            result = target.handle_message(msg);
            _callback = msg.get_callback();     #消息自身携带的回调(callable)对象;
            try:
                _callback(msg, result);         #函数或者实现了内置方法__call__的对象;
            except:
                _callback.execute(msg, result); #实现了接口Runnable的execute方法的对象;
        else:pass;
        
        self.set_running_flag(False);
        return 0;
    
    #分发消息:把消息分发给对应的消息处理器对象;
    def dispatch_message(self, msg):
        #STEP1:取出消息中携带的消息处理器对象;
        target = msg.get_target();
        
        #STEP2:调用该消息处理器对象来处理当前消息;
        result = target.handle_message(msg);
        
        #STEP3:取消息自身携带的回调对象,用于完成一些消息处理后的反馈;
        _callback = msg.get_callback();     #消息自身携带的回调(callable)对象;
        try:
            _callback(msg, result);         #函数或者实现了内置方法__call__的对象;
        except:
            _callback.execute(msg, result); #实现了接口Runnable的execute方法的对象;
        return True;
    
    def loop(self):
        self.set_running_flag(True);
        
        while(self.is_running()):
            msg = self.__queue.get();
            self.dispatch_message(msg);     #把消息分发给对应的消息处理器对象;
        else:pass;
        
        self.set_running_flag(False);
        return 0;

#消息处理器类:
class Handler:
    def __init__(self, _looper, _callback = None):
        self.__looper = _looper;
        self.__callback = _callback;
    
    def __del__(self):
        pass;
    
    #该函数留给子类实现:
    def handle_message(self, msg):
        print("WARN: the member handle_message() have not been implemented");
        return False;
    
    def send_message(self, _what, _id = -1, _target = None, _callback = None, _arg1 = 0, _arg2 = 0, _object = None):
        #def __init__(self, _what, _id = -1, _target = None, _callback = None, _arg1 = 0, _arg2 = 0, _object = None):
        __what = _what;
        __id = _id;
        if(__id <= 0):
            __id = time.time();
        else:pass;
        
        __target = _target;
        if(__target == None):
            __target = self;
        else:pass;
        
        __callback = _callback;
        if(__callback == None):
            __callback = self;
        else:pass;
        
        __arg1 = _arg1;
        __arg2 = _arg2;
        __object = _object;
        
        msg = Message(__what, __id, __target, __callback, __arg1, __arg2, __object);
        return msg.get_target().handle_message(msg);
    
    def post_message(self, _what, _id = -1, _target = None, _callback = None, _arg1 = 0, _arg2 = 0, _object = None):
        __what = _what;
        __id = _id;
        if(__id <= 0):
            __id = time.time();
        else:pass;
        
        __target = _target;
        if(__target == None):
            __target = self;
        else:pass;
        
        __callback = _callback;
        if(__callback == None):
            __callback = self;
        else:pass;
        
        __arg1 = _arg1;
        __arg2 = _arg2;
        __object = _object;
        
        msg = Message(__what, __id, __target, __callback, __arg1, __arg2, __object);
        self.__looper.enqueue(msg);
        return 0;

# class MyApp1(Handler, Runnable):
#     def __init__(self, _looper):
#         Handler.__init__(self, _looper);
#         
#     def __del__(self):
#         pass;
#     
#     def handle_message(self, msg):
#         _what = msg.get_what();
#         print("MyApp<1>处理消息WHAT = " + str(_what));
#         return True;
#     
#     def execute(self, msg, result):
#         _what = msg.get_what();
#         print("<1>处理消息WHAT = " + str(_what) + "have done, result = " + str(result));
#         return True;
#     
#     def run(self):
#         while(True):
#             time.sleep(3);
#             self.post_message(123, _callback = self);
#             time.sleep(2);
#             self.post_message(456, _target = app2, _callback = app2);
#             
# 
# class MyApp2(Handler, Runnable):
#     def __init__(self, _looper):
#         Handler.__init__(self, _looper);
#         pass;
#         
#     def __del__(self):
#         pass;
#     
#     def execute(self, msg, result):
#         _what = msg.get_what();
#         print("<2>处理消息WHAT = " + str(_what) + "have done, result = " + str(result));
#         return True;
#     
#     def handle_message(self, msg):
#         _what = msg.get_what();
#         print("MyApp<2>处理消息WHAT = " + str(_what));
#         return True;
# 
# #程序入口点:
# if __name__ == '__main__':
#     __looper = Looper.get_looper();
#     app1 = MyApp1(__looper);
#     app2 = MyApp2(__looper);
#     app1.run();

        
