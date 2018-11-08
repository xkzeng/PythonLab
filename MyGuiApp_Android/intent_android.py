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
    FLAG_NEED_CALLBACK = 1 << 2;
    def __init__(self, _what = 0, _target = None, _callback = None, _arg1 = 0, _arg2 = 0, _object = None):
        self.__id = time.time();
        self.__what = _what;
        self.__arg1 = _arg1;
        self.__arg2 = _arg2;
        self.__object = _object;
        self.__flags = 0;
        self.__target = _target;
        self.__callback = _callback; #Runnable
    
    def __del__(self):
        self.clear();
        
    def clear(self):
        self.__what = 0;
        self.__arg1 = 0;
        self.__arg2 = 0;
        self.__object = None;
        self.__flags = 0;
        self.__target = None;
        self.__callback = None;
        
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
    
    def set_object(self, _object):
        self.__object = _object;
        
    def need_callback(self):
        return (self.__flags & Message.FLAG_NEED_CALLBACK) != 0;
    
    def set_need_callback(self, _need_callback):
        if(_need_callback):
            self.__flags |= Message.FLAG_NEED_CALLBACK;
        else:
            self.__flags &= ~Message.FLAG_NEED_CALLBACK;

#消息循环线程:
class LooperThread(threading.Thread):
    def __init__(self, _looper = None):
        threading.Thread.__init__(self);
        self.name = "LooperThread";
        self.__looper = _looper;
        self.__cond = threading.Condition();
        
    def __del__(self):
        pass;
    
    def getLooper(self):
        if(self.isAlive() == False):
            return None;
        else:pass;
        
        self.__cond.acquire();
        if(self.__looper == None):
            print("looper is null, wait");
            self.__cond.wait();
        else:pass;
        self.__cond.release();
        
        return self.__looper;
    
    @staticmethod
    def newInstance():
        _looperThread = LooperThread();
        _looperThread.start();
        
        _looper = _looperThread.getLooper();
        if(_looper == None):
            raise RuntimeError("Looper is None");
        else:pass;
        return _looper;
    
    #重载的线程函数
    def run(self):
        print("thread %s start\n" % (self.getName()));
        Looper.prepare(True);
        
        self.__cond.acquire();
        self.__looper = Looper.myLooper();
        if(self.__looper != None):
            print("looper is prepared, notify others");
            self.__cond.notify();
        else:pass;
        self.__cond.release();
        
        Looper.loop();
        #self.__looper.cleanup();
        print("WARN: message loop unexpectedly exited");
        print("thread %s exit" % (self.getName()));

#消息循环类:
class Looper:
    stTLS = threading.local();
    stMainLooper = None;
    def __init__(self, quitAllowed):
        self.__running = True;
        self.__queue = MessageQueue();#消息队列;
        self.__lock = threading.Lock();
        self.__quitAllowed = quitAllowed;
        self.__thread = threading.currentThread();
        pass;
    
    def __del__(self):
        pass;
    
    @staticmethod
    def prepare(quitAllowed):
        if(hasattr(Looper.stTLS, "_looper") == True):
            raise AttributeError("Only one Looper may be created per thread");
        else:pass;
        Looper.stTLS._looper = Looper(quitAllowed);
        
    @staticmethod
    def myLooper():
        if(hasattr(Looper.stTLS, "_looper") == True):
            return Looper.stTLS._looper;
        else:
            return None;
    
    @staticmethod
    def prepareMainLooper():
        Looper.prepare(False);
        if(Looper.stMainLooper != None):
            raise AttributeError("The main Looper has already been prepared");
        else:pass;
        Looper.stMainLooper = Looper.myLooper();
    
    @staticmethod
    def getMainLooper():
        return Looper.stMainLooper;
    
    def getQueue(self):
        return self.__queue;
    
    @staticmethod
    def myQueue():
        return Looper.myLooper().getQueue();
    
    def getThread(self):
        return self.__thread;
    
    @staticmethod
    def get_looper():
        _looper = Looper(True);
        thrd = LooperThread(_looper);
        thrd.start();
        return _looper;
    
    def isQuitAllowed(self):
        return self.__quitAllowed;
    
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
        if(self.isQuitAllowed() == True):
            self.set_running_flag(False);
        else:
            print("the main looper do not be allowed to quit");
        return 0;
    
    def enqueue(self, msg):
        if(self.is_running()):
            self.__queue.put(msg);
            return True;
        else:
            print("this looper do not start");
            return False;
    
    #分发消息:把消息分发给对应的消息处理器对象;
    def dispatch_message(self, msg):
        #STEP1:取出消息中携带的消息处理器对象;
        _target = msg.get_target();
        
        #STEP2:调用该消息处理器对象来处理当前消息;
        result = _target.handle_message(msg);
        
        #STEP3:取消息自身携带的回调对象,用于完成一些消息处理后的反馈;
        _callback = msg.get_callback();     #消息自身携带的回调(callable)对象;
        if(_callback != None):
            try:
                _callback(msg, result);         #函数或者实现了内置方法__call__的对象;
            except:
                _callback.execute(msg, result); #实现了接口Runnable的execute方法的对象;
        else:
            if(msg.need_callback()):
                _target.message_callback(msg, result);
            else:pass;
        return True;
    
    @staticmethod
    def loop():
        _looper = Looper.myLooper();
        _queue = _looper.getQueue(); #Looper.myQueue();
        _looper.set_running_flag(True);
        
        msg = None;
        while(_looper.is_running()):
            msg = _queue.get();
            if(msg.get_what() <= 0):
                if(_looper.isQuitAllowed() == True):
                    print("the current looper quit");
                    break;
                else:
                    print("the main looper do not be allowed to quit");
                    continue;
            else:pass;
            _looper.dispatch_message(msg);     #把消息分发给对应的消息处理器对象;
        else:pass;
        
        _looper.set_running_flag(False);
        return 0;

#消息处理器类:
class MessageHandler:
    def __init__(self, _looper = None, _callback = None):
        if(_looper == None):
            self.__looper = Looper.myLooper();
            if(self.__looper == None):
                self.__looper = LooperThread.newInstance();
            else:pass;
        else:
            self.__looper = _looper;
        self.__callback = _callback;
    
    def __del__(self):
        pass;
    
    def getLooper(self):
        return self.__looper;
    
    #该函数留给子类实现:
    def filter_message(self, msg):
        print("WARN: the member MsgApp.filter_message() have not been implemented");
        return False;
    
    #该函数留给子类实现:
    def handle_message(self, msg):
        print("WARN: the member MessageHandler.handle_message() have not been implemented");
        return False;
    
    #该函数留给子类实现:
    def message_callback(self, msg, result):
        print("WARN: the member MessageHandler.message_callback() have not been implemented");
        return False;
    
    def send_message(self, what = 0, target = None, callback = None, arg1 = 0, arg2 = 0, obj = None, need_callback = False):
        __what = what;
        
        __target = target;
        if(__target == None):
            __target = self;
        else:pass;
        
        __callback = callback;
#         if(__callback == None):
#             __callback = self;
#         else:pass;
        
        __arg1 = arg1;
        __arg2 = arg2;
        __object = obj;
        
        #def __init__(self, _what = 0, _target = None, _callback = None, _arg1 = 0, _arg2 = 0, _object = None)
        msg = Message(_what = __what, _target = __target, _callback = __callback, _arg1 = __arg1, _arg2 = __arg2, _object = __object);
        msg.set_need_callback(need_callback);
        return msg.get_target().handle_message(msg);
    
    def post_message(self, what = 0,  target = None, callback = None, arg1 = 0, arg2 = 0, obj = None, need_callback = False):
        __what = what;
        
        __target = target;
        if(__target == None):
            __target = self;
        else:pass;
        
        __callback = callback;
#         if(__callback == None):
#             __callback = self;
#         else:pass;
        
        __arg1 = arg1;
        __arg2 = arg2;
        __object = obj;
        
        ##def __init__(self, _what = 0, _target = None, _callback = None, _arg1 = 0, _arg2 = 0, _object = None):
        msg = Message(_what = __what, _target = __target, _callback = __callback, _arg1 = __arg1, _arg2 = __arg2, _object = __object);
        msg.set_need_callback(need_callback);
        self.__looper.enqueue(msg);
        return 0;

class MsgApp(MessageHandler, Runnable):
    def __init__(self, _looper = None, _callback = None):
        #MessageHandler.__init__(self, LooperThread.newInstance(), _callback);
        MessageHandler.__init__(self, _looper, _callback);
        Runnable.__init__(self);
    
    def __del__(self):
        Runnable.__del__(self);
        MessageHandler.__del__(self);
    
    def filter_message(self, msg):
        print("WARN: the member MsgApp.filter_message() have not been implemented");
        return False;
    
    def handle_message(self, msg):
        _what = msg.get_what();
        print("MsgApp handle message " + str(_what));
        return True;
    
    def message_callback(self, msg, result):
        _what = msg.get_what();
        print("message " + str(_what) + " have done, result = " + str(result));
    
    def execute(self, msg, result):
        _what = msg.get_what();
        print("message " + str(_what) + " have done, result = " + str(result));
        return True;
    
    def __call__(self, msg, result):
        _what = msg.get_what();
        print("message " + str(_what) + " have done, result = " + str(result));
        return True;
    
#     def run(self):
#         _what1 = 100;
#         _what2 = 200;
#         while(True):
#             time.sleep(1);
#             self.post_message(what = _what1);
#             _what1 = _what1 + 1;
#             time.sleep(1);
#             self.post_message(what = _what2, need_callback = True);
#             _what2 = _what2 + 1;
# 
# class AppTest(MsgApp):
#     def __init__(self, _looper = None, _callback = None):
#         MsgApp.__init__(self);
#     
#     def __del__(self):
#         MsgApp.__del__(self);
#     
#     def filter_message(self, msg):
#         print("filter message %d" % (msg.get_what()));
#         return False;
#     
#     def handle_message(self, msg):
#         _what = msg.get_what();
#         print("AppTest handle message " + str(_what));
#         return True;
#     
#     def message_callback(self, msg, result):
#         _what = msg.get_what();
#         print("message " + str(_what) + " have done, result = " + str(result));
# 
# def doMain1():
#     Looper.prepareMainLooper();
#     app1 = MsgApp(Looper.getMainLooper());
#     t1 = threading.Thread(target=app1.run, name = "TestThread");
#     t1.start();
#     
#     t2 = threading.currentThread();
#     print(">>>>>> %s, %s" % (t1.getName(), t2.getName()));
#     Looper.loop();
# 
# def doMain2():
#     _looper = LooperThread.newInstance();
#     app1 = MsgApp(_looper);
#     app1.run();
# 
# def doMain3():
#     app1 = MsgApp();
#     app1.run();
# 
# def doMain4():
#     app1 = AppTest();
#     app1.run();
# 
# #程序入口点:
# if __name__ == '__main__':
#     #doMain1();
#     #doMain2();
#     doMain3();
#     #doMain4();
