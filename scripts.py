# -*- coding: utf-8 -*-
import os
import time
import re
from utils.rtext import *
scriptPath = 'D:/MCDaemon_windows-master/config/scripts/'
run = 0

class BOT:
    def RunScript(server, name):
        try:
            if run == 0:
                run = 1
            else:
                return 3
        except NameError:
            run = 0
        realPath = scriptPath + name
        if not os.path.exists(realPath):
            return None
        try:
            with open(realPath, 'r') as f:
                lines = f.read().split('\n')
                total = len(lines)
                done = 0
                ignore = 0
                for i in lines:
                    done = done + 1
                    if i.startswith('/'):
                        server.execute(i[1:])
                    elif re.match('sleep.[0-9]{1,2}$', i) != None:
                        time.sleep(int(i[6:]))
                    elif re.match('sleep..[0-9]{1}$', i) != None:
                        time.sleep(int(i[7:])/10)
                    else:
                        done = done - 1
                        ignore = ignore + 1
        except Exception as err:
            return err
            run = 0
        else:
            return total, done, ignore
            run = 0
    
    def saySlist(server, player):
        server.tell(player, '§6脚本文件列表：')
        for i in os.listdir(scriptPath):
            if re.match('.*.mcs', i):
                server.tell(player, RTextList(RText('[▷] ', color=RColor.green).h(f'点击运行§6{i}§r').c(RAction.run_command, f'!!bots run {i}'), i))
        
def on_user_info(server, info):
    if info.content.startswith('!!bots'):
        cmd = info.content.split(' ')
        cmdLen = len(cmd)
        if cmdLen == 2 and cmd[1] == 'list':
            BOT.saySlist(server, info.player)
        if cmdLen == 3 and cmd[1] == 'run':
            result = BOT.RunScript(server, cmd[2])
            if type(result) == tuple:
                time.sleep(1)
                server.tell(info.player, '文件总计行数{}，其中{}行被执行，{}行被忽略。'.format(result[0], result[1], result[2]))
            elif result is None:
                server.tell(info.player, '文件不存在。')
            elif result == 3:
                server.tell(info.player, '有脚本正在运行。')
            else:
                server.tell(info.player, '运行时发生错误。错误代码如下：\n{}'.format(result))
