import os
import sys
import time
import shutil
import ConfigParser

MT6572 = 'MT6572'
MT6582 = 'MT6582'

sw_file_list_72 = [
	'MBR',
	'EBR1',
	'lk.bin',
	'boot.img',                      
	'recovery.img',                      
	'secro.img',
	'logo.bin',
	'system.img',
	'cache.img',
	'userdata.img']
sw_file_list_82 = [
        'MBR',
	'EBR1',
	'EBR2',
	'lk.bin',
	'logo.bin',
        'boot.img',
	'recovery.img',
	'secro.img',
	'system.img',
        'cache.img',
	'userdata.img']

LAST_VER_NO_FILE_NAME = 'pac_last_ver_no'
FULL_VER_NO_FILE_NAME = 'full_ver_no'
SCATTER_WITH_FAT_FP = os.path.join('E:\\','release','common','MT6572_Android_scatter_fat.txt')
FAT_IMG_FN = 'fat_sparse.img'

def show_error(error_msg):
    print error_msg
    os.system('pause')
    sys.exit()
    
def check_usr_build_mode(path):
    makemtk_ini_path = os.path.join(path,'makeMtk.ini');
    makemtk_ini = open(makemtk_ini_path,'r')
    for line in makemtk_ini:
        line_ = line.split('=')
        if len(line_) == 2:
            key = line_[0].strip()
            value = line_[1].strip()
            print key,value
            if cmp(key,'build_mode') == 0 and cmp(value,'user') == 0:
                makemtk_ini.close()
                return True
    makemtk_ini.close()
    show_error('fatal error : not user build')

def get_sw_dl_list(plat,prj):
    sw_list = []
    if cmp(plat, MT6572) == 0:
        sw_list.extend(sw_file_list_72)
    elif cmp(plat, MT6582) == 0:
        sw_list.extend(sw_file_list_82)
    else:
        show_error('fatal error : unsupport platform')
        
    sw_list.append(plat+'_Android_scatter.txt')
    sw_list.append('preloader_'+prj+'.bin')
    return sw_list

def get_db_list(prj_path,plat,prj,android_ver):
    #prj_short = prj.split('_')[-1].upper()
    prj_short = 'JB3'
    db_file_list = []
    if android_ver.startswith('4.4'):
        apdb_name = 'APDB_'+plat+'_S01_KK1.MP7_'
        db_file1 = os.path.join('out','target','product',prj,'obj','CODEGEN','cgen',apdb_name)
        MODEM_OUT_PATH = os.path.join('out','target','product',prj,'obj','CUSTGEN','custom','modem')
    else:
        apdb_name = 'APDB_'+plat+'_S01_ALPS.'+prj_short+'.MP_'
        db_file1 = os.path.join('mediatek','cgen',apdb_name)
        MODEM_OUT_PATH = os.path.join('mediatek/custom/out',prj,'modem')
    db_file2 = db_file1+'_ENUM'
    db_file_list.append(db_file1)
    db_file_list.append(db_file2)
    
    modem_file_list = os.listdir(os.path.join(prj_path,MODEM_OUT_PATH))
    for modem_file in modem_file_list:
        if modem_file.startswith('BPLGUInfoCustomAppSrcP'):
            db_file_list.append(os.path.join(MODEM_OUT_PATH,modem_file))
            break
    return db_file_list

def do_cmd(cmd):
    print 'cmd :'+cmd
    os.system(cmd)

def cp_one_file(src_file,dst_dir):
    src_file_name = os.path.basename(src_file)
    dst_file = os.path.join(dst_dir,src_file_name)
    shutil.copyfile(src_file,dst_file)
    #do_cmd(' '.join(['copy',src_file,dst_file]))

def ota_dl(path,prj,dst_dir):
    out_path = os.path.join(path,'out','target','product',prj)
    ota_file_name = prj+'-ota-user.android.zip'
    cp_one_file(os.path.join(out_path,ota_file_name),dst_dir)

def get_last_sub_ver_int(ver_file,undef_value):
    ver_no = 0
    if os.path.exists(ver_file):
        last_custom_ver_file = open(ver_file)
        try:        
            ver_no = last_custom_ver_file.read().strip()
            ver_no = int(ver_no)
        finally:
            last_custom_ver_file.close()
    else:
        print 'last_update file not exists'
    return ver_no

def get_fromat_subver(sub_ver_int):
    if int(sub_ver_int) < 10:
        return '0'+str(sub_ver_int)
    return str(sub_ver_int)

def join_ver_str(pac_path,product,cust_name,cust_sub,main_ver,sub_ver):
    pac_name_list = [product]
    if len(cust_name) > 0:
        pac_name_list.append(cust_name)
    if len(cust_sub) > 0:
        pac_name_list.append(cust_sub)
    pac_name_list.extend([main_ver,get_fromat_subver(sub_ver),time.strftime('%y%m%d')])
    return '_'.join(pac_name_list)
    
def get_ver_str(pac_path,product,cust_name,cust_sub,main_ver):
    sub_ver_file = os.path.join(pac_path,LAST_VER_NO_FILE_NAME)
    sub_ver = get_last_sub_ver_int(sub_ver_file,0)+1
    return join_ver_str(pac_path,product,cust_name,cust_sub,main_ver,sub_ver)

def get_last_ver_str(pac_path,product,cust_name,cust_sub,main_ver,base_ver):
    sub_ver_file = os.path.join(pac_path,LAST_VER_NO_FILE_NAME)
    sub_ver = get_last_sub_ver_int(sub_ver_file,0)
    if sub_ver < 1:
        return base_ver    
    return join_ver_str(pac_path,product,cust_name,cust_sub,main_ver,sub_ver)

def check_fat_img(src_fat_img,dst_dir):
    img_name = os.path.basename(src_fat_img)
    dst_img = os.path.join(dst_dir,img_name)
    if os.path.exists(src_fat_img) and (not os.path.exists(dst_img)):
        cp_one_file(src_fat_img,dst_dir)
    dst_scatter_fp = os.path.join(dst_dir,'MT6572_Android_scatter.txt')
    if os.path.exists(dst_img) and os.path.exists(dst_scatter_fp):
        do_cmd(' '.join(['copy',SCATTER_WITH_FAT_FP,dst_scatter_fp]))
   
def check_build_version(prj_path,dl_path):
    build_prop_file = os.path.join(prj_path,"system",'build.prop')
    if not os.path.exists(build_prop_file):
        return
    build_prop = open(build_prop_file,'r')
    for line in build_prop:
        line_ = line.split('=')
        if len(line_) == 2:
            key = line_[0].strip()
            value = line_[1].strip()
            if cmp(key,'ro.build.display.id') == 0:
                sub_ver_file = os.path.join(dl_path,'..',FULL_VER_NO_FILE_NAME)
                os.system('echo '+value+' > '+sub_ver_file)
                break
    build_prop.close()

def check_android_version(prj_path,prj):
    android_ver = ''
    build_prop_file = os.path.join(prj_path,'out','target','product',prj,"system",'build.prop')
    if not os.path.exists(build_prop_file):
        return android_ver
    
    build_prop = open(build_prop_file,'r')
    for line in build_prop:
        line_ = line.split('=')
        if len(line_) == 2:
            key = line_[0].strip()
            value = line_[1].strip()
            
            if cmp(key,'ro.build.version.release') == 0:
                android_ver = value
                break
    build_prop.close()
    return android_ver

def start_dl(prj_path,dl_path,mtk_plat,mtk_prj):
    if not os.path.exists(dl_path):
        os.makedirs(dl_path)
        
    sw_file_list = get_sw_dl_list(mtk_plat,mtk_prj)
    for sw_file in sw_file_list:
        src_file = os.path.join(prj_path,sw_file)
        dst_file = os.path.join(dl_path,sw_file)
        cp_cmd = ' '.join(['copy',src_file,dst_file])
        do_cmd(cp_cmd)
        
    check_fat_img(FAT_IMG_FN,dl_path)
    check_build_version(prj_path,dl_path)
        
class pac_obj:
    prj_path = ''
    mtk_prj = ''
    mtk_plat = ''
    cust_name = ''
    cust_sub = ''
    product = ''
    main_ver = ''
    pac_path = '.'
    
    def __init__(self,path,prj,plat,name,sub_name,product,ver):
        self.prj_path = path
        self.mtk_prj = prj
        self.mtk_plat = plat
        self.cust_name = name
        self.cust_sub = sub_name
        self.product = product
        self.main_ver = ver

    def cp_prj_files(self,src_list, dst_dir):
        for src in src_list:
            cp_one_file(os.path.join(self.prj_path,src),dst_dir)

    def cp_prj_out_files(self,src_list, dst_dir):
        prj_out = 'out/target/product/'+self.mtk_prj
        for src in src_list:
            cp_one_file(os.path.join(self.prj_path,prj_out,src),dst_dir)

    def check_sum(self,path):
        check_sum_exe_file = 'CheckSum_Gen.exe'
        check_sum_exe_file_path = os.path.join('c:\\','hcj','tools',check_sum_exe_file)
        cp_one_file(check_sum_exe_file_path,path)
        os.chdir(path)
        do_cmd(check_sum_exe_file)
        do_cmd('del /f /q '+check_sum_exe_file)
        os.chdir('..')

    def get_rel_note_file_name(self,product,custom):
        name_list = ['release',product]
        if len(custom) > 0:
            name_list.append(custom)
        return '_'.join(name_list)+'.xls'

    def get_ver_str(self):  
        return get_ver_str(self.pac_path,self.product,self.cust_name, \
                                    self.cust_sub,self.main_ver)

    def get_last_ver_str(self,base_ver):
        return get_last_ver_str(self.pac_path,self.product,self.cust_name, \
                                    self.cust_sub,self.main_ver,base_ver)
            
    def start_pac(self):
        print 'check user build mode --------------'
        check_usr_build_mode(self.prj_path)
        android_ver = check_android_version(self.prj_path,self.mtk_prj)

        print 'gen pac name -----------------------'            
        pac_name = ''
        sub_ver_file = os.path.join('.',FULL_VER_NO_FILE_NAME)
        if os.path.exists(sub_ver_file):
            VER_FILE = open(sub_ver_file,'r')
            try:
                pac_name = VER_FILE.read().strip()
            finally:
                VER_FILE.close()
                os.system('del '+sub_ver_file)
        else:
            pac_name = get_ver_str(self.pac_path,self.product,self.cust_name, \
                                    self.cust_sub,self.main_ver)

        rel_note_file_name = self.get_rel_note_file_name(self.product,self.cust_name)

        print 'get copy file list-------------------'
        sw_file_list = get_sw_dl_list(self.mtk_plat,self.mtk_prj)
        
        #other_file_list = ['kernel/out/vmlinux']
        
        DATABASE_FILE_NAME = 'database'
        SOFTWARE_FILE_NAME = 'software'
        dst_database_path = os.path.join(self.pac_path,DATABASE_FILE_NAME)
        dst_software_path = os.path.join(self.pac_path,SOFTWARE_FILE_NAME)
        dst_other_path = self.pac_path

        if not os.path.exists(dst_software_path):
            print 'copy software begin------------------'
            os.makedirs(dst_software_path)
            self.cp_prj_out_files(sw_file_list,dst_software_path)
        is_del_database = True    
        if not os.path.exists(dst_database_path):
            print 'copy database begin------------------'
            db_file_list = get_db_list(self.prj_path,self.mtk_plat,self.mtk_prj,android_ver)
            os.makedirs(dst_database_path)
            self.cp_prj_files(db_file_list,dst_database_path)
        else:
            is_del_database = False
        #print 'copy other begin------------------'
        #self.cp_prj_files(other_file_list,self.pac_path)

        check_fat_img(FAT_IMG_FN,dst_software_path)
        
        pac_files_str = ' '.join([SOFTWARE_FILE_NAME,
                                 DATABASE_FILE_NAME])                                 
        
        print 'copy & exec CheckSum_Gen.exe------------------'
        self.check_sum(SOFTWARE_FILE_NAME)

        print 'create rar file begin------------------'
        win_rar_path = '\"C:\Program Files\WinRAR\WinRAR.exe\"'
        out_file_name = pac_name+'.rar'
        rar_cmd = win_rar_path+' a '+ out_file_name +' '+pac_files_str            
        do_cmd(rar_cmd)

        print 'delete temp files------------------'
        if is_del_database:
            os.system('del /f /q '+dst_database_path)
            #os.system('del /f /q '+dst_software_path)
            os.system('rd '+dst_database_path)
        #os.system('rd '+dst_software_path)
        os.system('del '+os.path.join(dst_software_path,'Checksum.ini'))

        print  'save current version no------------'
        os.system('echo '+sub_ver+' > '+sub_ver_file)

        os.system('pause')
        
