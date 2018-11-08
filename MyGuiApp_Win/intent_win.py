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
    def __init__(self, _what = 0, _arg1 = 0, _arg2 = 0, _object = None, _sender = None):
        self.__id = time.time();
        self.__what = _what;
        self.__arg1 = _arg1;
        self.__arg2 = _arg2;
        self.__object = _object;
        self.__flags = 0;
        self.__sender = _sender;
    
    def __del__(self):
        self.clear();
        
    def clear(self):
        self.__what = 0;
        self.__arg1 = 0;
        self.__arg2 = 0;
        self.__object = None;
        self.__flags = 0;
        self.__sender = None;
        
    def get_id(self):
        return self.__id;
    
    def set_id(self, msgId):
        self.__id = msgId;
        
    def get_what(self):
        return self.__what;
    
    def set_what(self, what):
        self.__what = what;
        
    def get_sender(self):
        return self.__sender;
    
    def set_sender(self, sender):
        self.__sender = sender;
        
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

#消息循环类:
class MessageLooper:
    def __init__(self, msgHandler, isAlone = True, quitAllowed = True):
        self.__running = True;
        self.__lock = threading.Lock();
        
        self.__queue = MessageQueue();#消息队列;
        self.__msgHandler = msgHandler;
        self.__isAlone = isAlone;
        self.__quitAllowed = quitAllowed;
    
    def __del__(self):
        pass;
    
    def queue(self):
        return self.__queue;
    
    def getQueue(self):
        return self.__queue;
    
    def isAlone(self):
        return self.__isAlone;
    
    def isQuitAllowed(self):
        return self.__quitAllowed;
    
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
    
    #分发消息:把消息分发给对应的消息处理器实例;
    def dispatch_message(self, msg):
        result = self.__msgHandler.handle_message(msg);
        
        if(msg.need_callback()):
            _sender = msg.get_sender();
            if(_sender != None):
                _sender.message_callback(msg, result);
            else:
                print("ERROR: sender is null, can not do it's callback!");
        else:pass;
            
        return result;
    
    def loop(self):
        _queue = self.__queue;
        self.set_running_flag(True);
        
        msg = None;
        while(self.is_running()):
            msg = _queue.get();
            if(msg.get_what() <= 0):
                if(self.isQuitAllowed() == True):
                    print("the current looper quit");
                    break;
                else:
                    print("the main looper do not be allowed to quit");
                    continue;
            else:pass;
            self.dispatch_message(msg);     #把消息分发给对应的消息处理器实例;;
        else:pass;
        
        self.set_running_flag(False);
        return 0;

#消息循环线程:
class MsgApp(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self);
        self.name = "LooperThread";
        self.__looper = None;
        self.__queue = None;
        
    def __del__(self):
        pass;
    
    def send_message(self, what = 0, arg1 = 0, arg2 = 0, obj = None, need_callback = False, sender = None):
        __what = what;
        __arg1 = arg1;
        __arg2 = arg2;
        __object = obj;
        __sender = sender;
        
        #Message(self, _what = 0, _arg1 = 0, _arg2 = 0, _object = None, _sender = None):
        msg = Message(_what = __what, _arg1 = __arg1, _arg2 = __arg2, _object = __object, _sender = __sender);
        msg.set_need_callback(need_callback);
        return self.__looper.dispatch_message(msg);
    
    def post_message(self, what = 0, arg1 = 0, arg2 = 0, obj = None, need_callback = False, sender = None):
        __what = what;
        __arg1 = arg1;
        __arg2 = arg2;
        __object = obj;
        __sender = sender;
        
        #Message(self, _what = 0, _arg1 = 0, _arg2 = 0, _object = None, _sender = None):
        msg = Message(_what = __what, _arg1 = __arg1, _arg2 = __arg2, _object = __object, _sender = __sender);
        msg.set_need_callback(need_callback);
        #self.__looper.enqueue(msg);
        self.__queue.put(msg);
        return 0;
    
    #该函数留给子类实现:
    def filter_message(self, msg):
        print("WARN: the member MsgApp.filter_message() have not been implemented");
        return False;
    
    #该函数留给子类实现:
    def handle_message(self, msg):
        print("WARN: the member MsgApp.handle_message() have not been implemented");
        return False;
    
    #该函数留给子类实现:
    def message_callback(self, msg, result):
        print("WARN: the member MsgApp.message_callback() have not been implemented");
        return False;
    
    def runAsAlone(self):
        print("run as alone");
        self.__looper = MessageLooper(self);
        self.__queue = self.__looper.getQueue();
        self.setDaemon(True);
        self.start();
    
    def runAsMain(self):
        print("run as main");
        self.__looper = MessageLooper(self, isAlone = False, quitAllowed = False);
        self.__queue = self.__looper.getQueue();
        self.run();
        
    def runForEver(self, _isAlone = True, _quitAllowed = True):
        self.__looper = MessageLooper(self, isAlone = _isAlone, quitAllowed = _quitAllowed);
        self.__queue = self.__looper.getQueue();
        
        if(self.__looper.isAlone() == True):
            self.setDaemon(True);
            self.start();
        else:
            self.run();
    
    #重载的线程函数
    def run(self):
        print("thread %s start" % (self.getName()));
        self.__looper.loop();
        print("WARN: message loop unexpectedly exited");
        print("thread %s exit" % (self.getName()));

class AppTest1(MsgApp):
    def __init__(self):
        MsgApp.__init__(self);
    
    def __del__(self):
        MsgApp.__del__(self);
        
    def filter_message(self, msg):
        print("AppTest1 filtered message");
        return False;
    
    def handle_message(self, msg):
        _what = msg.get_what();
        print("AppTest1 handle message " + str(_what));
        return True;
    
    def message_callback(self, msg, result):
        _what = msg.get_what();
        print("AppTest1 message " + str(_what) + " have done, result = " + str(result));
    
    def makeMessage(self, sender = None):
        _what1 = 100;
        _what2 = 200;
        while(True):
            time.sleep(1);
            self.post_message(what = _what1);
            _what1 = _what1 + 1;
            time.sleep(1);
            self.post_message(what = _what2, need_callback = True, sender = sender);
            _what2 = _what2 + 1;

class AppTest2(MsgApp):
    def __init__(self):
        MsgApp.__init__(self);
    
    def __del__(self):
        MsgApp.__del__(self);
        
    def filter_message(self, msg):
        print("AppTest2 filtered message");
        return False;
    
    def handle_message(self, msg):
        _what = msg.get_what();
        print("AppTest2 handle message " + str(_what));
        return True;
    
    def message_callback(self, msg, result):
        _what = msg.get_what();
        print("AppTest2 message " + str(_what) + " have done, result = " + str(result));

def doMain1():
    app1 = AppTest1();
    t1 = threading.Thread(target = app1.makeMessage, kwargs={"sender":app1}, name = "Test1Thread");
    t1.start();
    app1.runAsAlone();
    app1.join();

def doMain2():
    app1 = AppTest1();
    t1 = threading.Thread(target = app1.makeMessage, kwargs={"sender":app1}, name = "Test2Thread");
    t1.start();
    app1.runAsMain();

def doMain3():
    app1 = AppTest1();
    app1.runForEver();
    t1 = threading.Thread(target = app1.makeMessage, kwargs={"sender":app1}, name = "Test3Thread");
    t1.start();
    app1.join();

def doMain4():
    app1 = AppTest1();
    t1 = threading.Thread(target = app1.makeMessage, kwargs={"sender":app1}, name = "Test3Thread");
    t1.start();
    app1.runForEver(_isAlone = False, _quitAllowed = False);

def doMain5():
    app1 = AppTest1();
    app2 = AppTest2();
    t1 = threading.Thread(target = app1.makeMessage, kwargs={"sender":app2}, name = "Test3Thread");
    t1.start();
    app1.runForEver();
    app2.runForEver();
    app1.join();

#程序入口点:
if __name__ == '__main__':
    doMain1();
    #doMain2();
    #doMain3();
    #doMain4();
    #doMain5();
    print("exit");
