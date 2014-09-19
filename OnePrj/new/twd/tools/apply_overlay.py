#!/usr/bin/python

import sys
import os
import commands

is_overlay = -1
boot_logo = ''
cust_name = ''
mm_path = ''

twd_project = os.getenv('TWD_PROJECT')
cust_name = os.getenv('TWD_CUST_NAME')
boot_logo = os.getenv('BOOT_LOGO')
mm_path = os.getenv('MM_PATH')

def show_usage():
    print 'Usage:\n' \
    'apply_overlay.py <flag>\n' \
    'flag: only 1/0 , 1 means overlay while 0 means restore'

def parse_args():
    global cust_name
    global boot_logo
    global mm_path
    global is_overlay
    for i in range(1,len(sys.argv)):
        arg = sys.argv[i]
        pair = arg.split('=');
        if len(pair) != 2:
            continue
        if cmp(pair[0],'cust') == 0:
            cust_name = pair[1]
        elif cmp(pair[0],'logo') == 0:
            boot_logo = pair[1]
        elif cmp(pair[0],'mm_path') == 0:
            mm_path = pair[1]
        elif cmp(pair[0],'is_overlay') == 0:
            is_overlay = int(pair[1])

def is_empty(value):
    return len(value) == 0

if len(sys.argv) < 2:
    show_usage()
    sys.exit(1)

parse_args()
print \
'cust_name='+cust_name \
+',boot_logo='+boot_logo \
+',mm_path='+mm_path \
+',is_overlay='+str(is_overlay) 

if(is_empty(cust_name)
   or is_empty(boot_logo)
   or is_overlay < 0):
    show_usage()
    sys.exit('please check your args!!!!!!!!!!!!')

CUST_ROOT_PATH = os.path.join('twd','custom',twd_project)
customer_path = os.path.join(CUST_ROOT_PATH,cust_name,'overlay')
cust_logo_path = os.path.join(CUST_ROOT_PATH,cust_name,'prebuilt','pwranim',boot_logo)
mm_full_path = ''
if not is_empty(mm_path):
    mm_full_path = os.path.join(customer_path,mm_path)

BACKUP_DIR = os.path.join('twd','backup')
BACKUP_ADD_FILE = 'add_files'
logo_path = 'mediatek/custom/common/lk/logo'
UBOOT_LOGO_FILE = boot_logo+'_uboot.bmp'
KERNEL_LOGO_FILE = boot_logo+'_kernel.bmp'
UBOOT_LOGO_PATH = os.path.join(logo_path,boot_logo,UBOOT_LOGO_FILE)
KERNEL_LOGO_PATH = os.path.join(logo_path,boot_logo,KERNEL_LOGO_FILE)
  
def do_cmd(cmd):
    status,output = commands.getstatusoutput(cmd)
    #return str(status)
    if(status != 0):
        print 'cmd: '+cmd+'\n'+'status='+str(status)+',output='+output        
        sys.exit(1)

def do_cmd_ignore_error(cmd):
    status,output = commands.getstatusoutput(cmd)
    #return str(status)
    if(status != 0):
        print 'cmd: '+cmd+'\n'+'status='+str(status)+',output='+output        

overlay_files_list = []
def callback(arg, directory, files):
    for file_ in files:
        #ignore files in root dir
        if cmp(arg,directory) == 0:
            continue
        file__ = os.path.join(directory, file_)
        if(os.path.isfile(file__)):
            overlay_files_list.append(file__[len(arg)+1:])           


def cp_file(src_file, dst_file):
    if os.path.exists(src_file):
        dst_path = os.path.dirname(dst_file)
        if not os.path.exists(dst_path):
            do_cmd('mkdir -p '+dst_path)            
        do_cmd('cp '+src_file+' '+dst_file)
        
def backup_overlay_files(files_list,backup_dir):
    if not os.path.exists(backup_dir):
        do_cmd('mkdir '+BACKUP_DIR)
    add_files_str = ''
    for src_file in files_list:
        dst_file = os.path.join(BACKUP_DIR,src_file)
        if os.path.exists(src_file):
            cp_file(src_file,dst_file)
        else:
            add_files_str += src_file+'\n'    
    if len(add_files_str) > 0:
        print('twd customer add files:\n'+add_files_str)
        add_file = open(os.path.join(backup_dir,BACKUP_ADD_FILE),'w')
        add_file.write(add_files_str)
        add_file.close()
    #special backup for logo
    cp_file(UBOOT_LOGO_PATH,os.path.join(BACKUP_DIR,UBOOT_LOGO_PATH))
    cp_file(KERNEL_LOGO_PATH,os.path.join(BACKUP_DIR,KERNEL_LOGO_PATH))
        
def backup_del_add_files(backup_dir):
    add_file_path = os.path.join(backup_dir,BACKUP_ADD_FILE)
    if os.path.exists(add_file_path):
        add_file = open(add_file_path,'r')
        for add_file_ in add_file:
            add_file__ = add_file_.strip()
            do_cmd_ignore_error('rm '+add_file__) 

def apply_overlay_files(files_list,src_path):    
    for dst_file in files_list:
        src_file = os.path.join(src_path,dst_file)
        cp_file(src_file,dst_file)
    #special overlay logo
    if cmp(src_path,BACKUP_DIR) == 0:
        src_logo_path = src_path
    else:
        src_logo_path = cust_logo_path
    cp_file(os.path.join(src_logo_path,UBOOT_LOGO_FILE),UBOOT_LOGO_PATH)
    cp_file(os.path.join(src_logo_path,KERNEL_LOGO_FILE),KERNEL_LOGO_PATH)
        
def gt_overlay():
    overlay_path = customer_path
    if not is_empty(mm_full_path):
        if os.path.exists(mm_full_path):
            overlay_path = mm_full_path
        else:
            print 'mm path is not exists in overlay path......'
            return
    print 'twd overlay .......'
    os.path.walk(overlay_path, callback, customer_path)  
    backup_overlay_files(overlay_files_list,BACKUP_DIR)
    apply_overlay_files(overlay_files_list,customer_path)
    
def gt_restore():
    print 'twd restore .......'
    os.path.walk(BACKUP_DIR, callback, BACKUP_DIR)
    backup_del_add_files(BACKUP_DIR)
    apply_overlay_files(overlay_files_list,BACKUP_DIR)
    os.system('rm -rf '+BACKUP_DIR)

def check_last_restore_done():
    print 'check_last_restore_done .......'
    if os.path.exists(BACKUP_DIR):
        print 'last restore undone .......'
        gt_restore()
    
if(is_overlay == 1):
    check_last_restore_done()
    gt_overlay()
else:
    gt_restore()

