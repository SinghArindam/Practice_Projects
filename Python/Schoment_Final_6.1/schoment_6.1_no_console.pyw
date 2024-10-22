import tkinter,mysql.connector,tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbx

from mysql.connector import cursor 

#   RDBMS (mysql) connectivity related
_port=3306
_password='root'


try:
    mydb = mysql.connector.connect(host="localhost",
                                   port=_port,
                                   user="root",
                                   password=_password)
    mydb.cursor().execute("create database schoment")
except:
    pass

mydb = mysql.connector.connect(host="localhost",
                               port=_port,
                               user="root",
                               password=_password,
                               database='schoment')

mycursor=mydb.cursor()

#   First screen showing welcome to Schoment, with next Button
def welcome():
    global screen_welcome
    screen_welcome = Tk()
    screen_welcome.geometry('300x360')
    screen_welcome.title('WELCOME')
    c=Canvas(screen_welcome,width=300,height=360)
    img=PhotoImage(file='ppm/welcm.ppm')
    image=c.create_image(1,1,anchor=NW,image=img)
    b=Button(text='Next',padx='133',bg='#DEDDDF',fg="black",font='helvetica',command=main_screen)
    b.pack(side=BOTTOM)
    c.create_window(148,350,window=b)
    c.pack()
    screen_welcome.mainloop()

#   Second Screen - Login and Register Buttons
def main_screen():
    try:
        screen_welcome.destroy()
    except:
        pass
    global screen
    screen = Tk()
    screen.geometry('300x350')
    screen.title("Description")
    
    canvas=Canvas(screen,width=300,height=400)
    img=PhotoImage(file='ppm/log+reg3.ppm')
    image=canvas.create_image(0,0,anchor=NW,image=img)
    canvas.pack()
    
    l1=Label(screen,text="If you are already an\nuser then please press LOGIN.",font='helvetica')
    l2=Label(screen,text='If you are an new user then\nplease press Register to get started.',font='helvetica')
    b1=Button(screen,text = 'Login', bg = '#fcaeca', activebackground='#F33DC3',font="Times",command=login)
    b2=Button(screen,text = 'Register', bg = '#9BFCF3',activebackground='#00E9D2',font="Times",command=register)

    canvas.create_window(154,210,window=l1)
    canvas.create_window(152,260,window=l2)
    canvas.create_window(80,310,window=b1)
    canvas.create_window(220,310,window=b2)
    screen.mainloop()

#   Register Screen - Screen 3r
def register():
    try:
        mycursor.execute("create table users(username varchar(25) unique,password varchar(25),post varchar(25))")
    except:
        pass
    
    global screen_reg
    screen_reg = Toplevel(screen)
    screen_reg.title('Register')
    screen_reg.geometry('300x250')

    screen.wm_state('iconic')       #   Minimizes the screen 'screen' as soon as 'screen_login' is created

    global username 
    global password 
    global post
    global username_entry
    global password_entry
    global post_entry
    
    username = StringVar()
    password = StringVar()
    post=StringVar()

    global cns
    cns=Canvas(screen_reg,width=300,height=250)
    img=PhotoImage(file='ppm/bb.ppm')
    image=cns.create_image(1,1,anchor=NW,image=img)
    cns.pack()
    
    z2=Label(screen_reg,
             text = 'Username *',
             font=('fenix',12),
             padx=7)
    
    username_entry = Entry(screen_reg,
                           textvariable = username,
                           width=17,
                           font=('arial',13))
    
    username_entry.pack()
    username = username_entry
    
    z3=Label(screen_reg,
             text = 'Password *',
             font=('fenix',12),
             padx=8)
    
    password_entry = Entry(screen_reg,
                           textvariable = password,
                           width=17,
                           font=('arial',13))

    password_entry.pack()
    password = password_entry

    z6=Label(screen_reg,
             text='Post *',
             font=('fenix',12),
             padx=25)

    post_entry = ttk.Combobox(screen_reg, width=17,textvariable=post,state='readonly')
    post_entry['values'] = ('Admin','Teacher')  #   A tuple is to be assigned as the values to be displayed
    post_entry.pack()
    post_entry.current(0)       #   Defining Initial state of Combobox
    
    z4=Button(screen_reg,
              text ='Register!',
              width =10, height = 1,
              bg='#9E9E9E',fg='white',
              font=('helvetica',10),command = register_user)
    
    z5=Button(screen_reg,text ='Back',width =5, height = 1,
              bg='#9E9E9E',fg='white',font=('helvetica',10),command = lambda : back_to_screen(screen_reg))

    cns.create_window(70,67,window=z2)
    cns.create_window(70,111,window=z3)
    cns.create_window(70,155,window=z6)
    cns.create_window(195,67,window=username_entry )
    cns.create_window(195,111,window=password_entry)
    cns.create_window(195,155,window=post_entry)
    cns.create_window(150,190,window=z4)
    cns.create_window(150,230,window=z5)
    screen_reg.mainloop()

#   Register Backend - append user data
def register_user():
    username_info = (username.get()).lower()
    password_info = (password.get()).lower()
    post_info = (post.get()).lower()

    if 8>len(username_info)>0 or 0<len(password_info)<8:
        tkinter.messagebox.showerror("Not Secure","Username and Password must have minimum 8 digits")   
    elif len(username_info)==0 or len(password_info)==0:
        tkinter.messagebox.showerror("Empty","Filling Username and Password are mandatory!")
    elif len(username_info)>=8 and len(password_info)>=8:
        mycursor.execute("select username from users where username='%s'"%(username_info))
        res=mycursor.fetchall()
        if len(res)==0:
            dat="insert into users(username,password,post) values(%s,%s,%s)"
            val=(username_info,password_info,post_info)
            mycursor.execute(dat,val)
            mydb.commit()
            tkinter.messagebox.showinfo("Success","You have been successfully registered :)")
            screen_reg.destroy()
            screen.deiconify()
        else:
            tkinter.messagebox.showerror("Already exists","The username has already been used please try something else")
    
# Login Screen - Screen 3l
def login():
    global screen_login
    screen_login = Toplevel(screen)
    screen_login.title('Login')
    screen_login.geometry('280x250')
    
    screen.wm_state('iconic')       #   Minimizes the screen 'screen' as soon as 'screen_login' is created

    global username_verify
    global password_verify
    global username_entry1
    global password_entry1
    username_verify = StringVar()
    password_verify = StringVar()

    global cnv
    cnv=Canvas(screen_login,width=280,height=250)
    img=PhotoImage(file='ppm/loginbg.ppm')
    image=cnv.create_image(1,1,anchor=NW,image=img)
    cnv.pack()

    
    l1_log=Label(screen_login,
                 text = 'Username *',
                 font=('fenix',11),
                 padx=7,
                 bg='white')
    
    username_entry1 = Entry(screen_login,
                            textvariable = username_verify,
                            width=17,
                            font=('arial',13))
    username_entry1.pack()

    username_entry1.focus()         #   makes the default position of Cursor in this entry so that user need not click this box before typing $$$$ not working

    l2_log=Label(screen_login,
                 text = 'Password *',
                 font=('fenix',11),
                 padx=8,
                 bg='white')
    
    password_entry1 = Entry(screen_login,
                            textvariable = password_verify,
                            width=17,
                            font=('arial',13))
    
    password_entry1.pack()
    b_log=Button(screen_login,
                 text = 'Login!',
                 width =10, height = 1,
                 bg='white',fg='black',
                 font=('fenix',11),
                 command = login_verify)
    
    back=Button(screen_login,
              text ='Back',
              width =5, height = 1,
              bg='#9E9E9E',fg='white',
              font=('helvetica',10),
              command = lambda : back_to_screen(screen_login))

    
    cnv.create_window(62,82,window=l1_log)
    cnv.create_window(62,126,window=l2_log)
    cnv.create_window(187,82,window=username_entry1 )
    cnv.create_window(187,126,window=password_entry1)
    cnv.create_window(137,190,window=b_log)
    cnv.create_window(137,230,window=back)
    screen_login.mainloop()

# Login Backend - verify credentials
def login_verify(): 
    username1 = username_verify.get()
    password1 = password_verify.get()

    if 8>len(username1)>0 and 0<len(password1)<8:
        tkinter.messagebox.showerror("Not Secure","Username and Password must have minimum 8 digits")   
    elif len(username1)==0 or len(password1)==0:
        tkinter.messagebox.showerror("Empty","Filling Username and Password are mandatory!")
    elif len(username1)>=8 and len(password1)>=8:
        _dat="select * from users where username='%s' and password='%s'"
        _stat=_dat%(username1,password1)
        mycursor.execute(_stat)
        result = mycursor.fetchall()
        if len(result)==0:
            tkinter.messagebox.showerror("Not Found","Please check your credentials again")
        else:
            if result[0][2]=='teacher':
                teacher('Teacher\'s DashBoard')
            elif result[0][2]=='admin': 
                admin()

    username_entry1.delete(0,END)
    password_entry1.delete(0,END)

try:
        mycursor.execute("create table students(admn_no integer,name varchar(25),dob date, contact bigint, father_name varchar(25),mother_name varchar(25))")
        mycursor.execute("create table teachers(t_no integer,name varchar(25),dob date, contact bigint, father_name varchar(25),mother_name varchar(25))")
except:
        pass


#   Dashboard - for Teachers
def teacher(title): 
    global t_screen
    try:
        t_screen.destroy()
    except:
        pass
    title = 'Teacher - Student Data'
    try:
        screen_login.destroy()
        screen.destroy()
    except:
        pass

    try:
        t_screen=Toplevel(adm_screen)
    except:
        t_screen=Tk()

    t_screen.geometry('900x600')
    t_screen.title(title)
    t_screen.resizable(False,False)

    global t_can
    t_can=Canvas(t_screen,width=900,height=600)
    img=PhotoImage(file='ppm/teacherbg.ppm')
    image_t =t_can.create_image(0,0,anchor=NW,image=img)
    t_can.pack()

    #search bar
    global se
    se=StringVar()
    t_search=Button(t_screen,
                    text='Search',
                    font=('fenix',12),
                    command=search_stu)
    search_entry=Entry(t_screen,
                       textvariable=se,
                       font=('Fenix',13))
    search_entry.pack()
    se=search_entry
    _se=Label(t_screen,text='Search by Name',font=('fenix',11))

    display_student()   # display (search) data

    # add student
    t_add=Button(t_screen,text='Add Student',font=('fenix',13),command=t_addstudent)
    # update student
    t_upd=Button(t_screen,text='Update',font=('fenix',13),command=lambda:t_updatestudent(''))
    # Delete Student
    t_del=Button(t_screen,text='Delete Student',font=('fenix',13),command=t_delstudent)
    # Exit
    t_ex=Button(t_screen,text='Exit',font=('fenix',13),command=exit_pro)
    # Hint label
    l_upd=Label(t_screen,text='You can double click to EDIT/UPDATE any entry.')
    
    #placing everything
    t_can.create_window(110,30,window=search_entry)
    t_can.create_window(245,30,window=t_search)
    t_can.create_window(110,55,window=_se)
    t_can.create_window(490,30,window=t_ex)
    t_can.create_window(680,30,window=t_del)
    t_can.create_window(560,30,window=t_upd)
    t_can.create_window(820,30,window=t_add)
    t_can.create_window(530,60,window=l_upd)
    
    t_screen.mainloop()

def back_to_adm_dash():
    t_screen.destroy()
    admin()
    
def search_stu():
    search_info=(se.get()).lower()
    mycursor.execute('select * from students where name=\'%s\''%search_info)
    result=mycursor.fetchall()
    if len(result)==0:
        tkinter.messagebox.showerror('Not Found','No student found!')
    else:
        search_display_s(result)  
    
def display_student(): 
    # Displays records in tabular form, written separately to ease ediions
    table_frame=Frame(t_screen,bd=4,relief=RIDGE,bg='azure')
    table_frame.place(x=10,y=70,width=875,height=520)
          
    scroll_x=Scrollbar(table_frame,orient=HORIZONTAL)
    scroll_y=Scrollbar(table_frame,orient=VERTICAL)

    global student_table
    student_table=ttk.Treeview(table_frame,columns=('admn_no','name','dob','contact','f_name','m_name'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

    scroll_x.pack(side=BOTTOM,fill=X)
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_x.config(command=student_table.xview)
    scroll_y.config(command=student_table.yview)
    
    student_table.heading('admn_no',text='Admission No')
    student_table.heading('name',text='Name')
    student_table.heading('dob',text='DOB')
    student_table.heading('contact',text='Contact No')
    student_table.heading('f_name',text='Father\'s Name')
    student_table.heading('m_name',text='Mother\'s name')
    student_table['show']='headings'  # To hide first column of index of data (metadata)
    student_table.column('admn_no',width=110)
    student_table.column('name',width=150)
    student_table.column('dob',width=130)
    student_table.column('contact',width=150)
    student_table.column('f_name',width=150)
    student_table.column('m_name',width=150)
    student_table.pack(fill=BOTH,expand=1)
    student_table.bind('<Double-Button-1>',t_updatestudent)
    fetch_table_data_s()

def fetch_table_data_s():
    mycursor.execute('select * from students order by admn_no')
    rows=mycursor.fetchall()
    global student_table
    if rows!=0:
        try:
            student_table.delete(student_table.get_children())
        except :
            pass
        for row in rows:
            student_table.insert('',END,values=row)

def t_addstudent():
    t_screen.iconify()
    global add_screen
    add_screen=Toplevel(t_screen)
    add_screen.geometry('400x400')
    add_screen.title('Add Student')

    global add_can
    add_can=Canvas(add_screen,width=400,height=400)
    img=PhotoImage(file='ppm/addbg.ppm')
    image=add_can.create_image(-200,0,anchor=NW,image=img)
    add_can.pack()

    global admn_no
    global name
    global dob
    global contact
    global f_name
    global m_name

    admn_no = StringVar()
    name=StringVar()
    dob=StringVar()
    contact=StringVar()
    f_name=StringVar()
    m_name=StringVar()

    admn_no_entry=Entry(add_screen,textvariable='admn_no',font=('Fenix',12))
    name_entry=Entry(add_screen,textvariable='name',font=('Fenix',12))
    dob_entry=Entry(add_screen,textvariable='dob',font=('Fenix',12))
    contact_entry=Entry(add_screen,textvariable='contact',font=('Fenix',12))
    f_name_entry=Entry(add_screen,textvariable='f_name',font=('Fenix',12))
    m_name_entry=Entry(add_screen,textvariable='m_name',font=('Fenix',12))

    admn_no_entry.delete(0,END)
    name_entry.delete(0,END)
    dob_entry.delete(0,END)
    contact_entry.delete(0,END)
    f_name_entry.delete(0,END)
    m_name_entry.delete(0,END)

    admn_no=admn_no_entry
    name=name_entry
    dob=dob_entry
    contact=contact_entry
    f_name=f_name_entry
    m_name=m_name_entry

    _admn_no=Label(add_screen,text='Admission No',font=('fenix',12))
    _name=Label(add_screen,text='Name',font=('fenix',12))
    _dob=Label(add_screen,text='DOB(YYYY-MM-DD)',font=('fenix',12))
    _contact=Label(add_screen,text='Contact',font=('fenix',12))
    _f_name=Label(add_screen,text='Father Name',font=('fenix',12))
    _m_name=Label(add_screen,text='Mother Name',font=('fenix',12))

    add_stu_b=Button(add_screen,text='Add Student',font=('Fenix',15),command=add_stu)
    add_stu_b_back=Button(add_screen,text='Back',font=('Fenix',12),command=back_and_deicon)

    add_can.create_window(80,30,window=_admn_no)
    add_can.create_window(80,70,window=_name)
    add_can.create_window(80,110,window=_dob)
    add_can.create_window(80,150,window=_contact)
    add_can.create_window(80,190,window=_f_name)
    add_can.create_window(80,230,window=_m_name)

    add_can.create_window(250,30,window=admn_no_entry)
    add_can.create_window(250,110,window=dob_entry)
    add_can.create_window(250,70,window=name_entry)
    add_can.create_window(250,150,window=contact_entry)
    add_can.create_window(250,190,window=f_name_entry)
    add_can.create_window(250,230,window=m_name_entry)

    add_can.create_window(200,330,window=add_stu_b)
    add_can.create_window(200,380,window=add_stu_b_back)

    add_screen.mainloop()

def back_and_deicon():
    add_screen.destroy()
    t_screen.deiconify()
def back_and_deicon2():
    t_d_screen.destroy()
    adm_screen.deiconify()
def back_and_deicon3():
    t_s_screen.destroy()
    adm_screen.deiconify()
def back_and_deicon4():
    add_student_a_screen.destroy()
    t_s_screen.deiconify()

def add_stu():
    admn_no_info=(admn_no.get()).lower()
    name_info=(name.get()).lower()
    dob_info=(dob.get()).lower()
    contact_info=(contact.get()).lower()
    f_name_info=(f_name.get()).lower()
    m_name_info=(m_name.get()).lower()
    if len(admn_no_info)==0 or len(name_info)==0 or len(dob_info)==0 or len(contact_info)==0 or len(f_name_info)==0 or len(m_name_info)==0:
        tkinter.messagebox.showerror('Empty','Filing all fields is mandatory!')
    else:
        mycursor.execute("insert into students value('%s','%s','%s','%s','%s','%s')"%(admn_no_info,name_info,dob_info,contact_info,f_name_info,m_name_info))
        mydb.commit()
        tkinter.messagebox.showinfo('Success','Successfully added student to the database!')
        teacher('')

def t_updatestudent(ev):
    cursor_row=student_table.focus()
    content=student_table.item(cursor_row)
    row=content['values']

    if len(cursor_row)==0:
        msgbx.showerror('Error','No Record selected')
        return
    
    global win_update
    win_update=Toplevel(t_screen)
    win_update.title('Update Details')
    win_update.geometry('400x400')

    global upd_can
    upd_can=Canvas(win_update,width=400,height=400)
    img=PhotoImage(file='ppm/addbg.ppm')
    image=upd_can.create_image(-200,0,anchor=NW,image=img)
    upd_can.pack()

    global admn_no
    global name
    global dob
    global contact
    global f_name
    global m_name

    admn_no = name=dob=contact=f_name=m_name=''

    admn_no = StringVar()
    name=StringVar()
    dob=StringVar()
    contact=StringVar()
    f_name=StringVar()
    m_name=StringVar()

    global admn_no_entry
    global name_entry
    global dob_entry
    global contact_entry
    global f_name_entry
    global m_name_entry

    admn_no_entry=Entry(win_update,textvariable='admn_no',font=('Fenix',12))
    name_entry=Entry(win_update,textvariable='name',font=('Fenix',12))
    dob_entry=Entry(win_update,textvariable='dob',font=('Fenix',12))
    contact_entry=Entry(win_update,textvariable='contact',font=('Fenix',12))
    f_name_entry=Entry(win_update,textvariable='f_name',font=('Fenix',12))
    m_name_entry=Entry(win_update,textvariable='m_name',font=('Fenix',12))

    admn_no_entry.delete(0,END)
    name_entry.delete(0,END)
    dob_entry.delete(0,END)
    contact_entry.delete(0,END)
    f_name_entry.delete(0,END)
    m_name_entry.delete(0,END)

    admn_no_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    dob_entry.insert(0,row[2])
    contact_entry.insert(0,row[3])
    f_name_entry.insert(0,row[4])
    m_name_entry.insert(0,row[5])

    admn_no=admn_no_entry
    name=name_entry
    dob=dob_entry
    contact=contact_entry
    f_name=f_name_entry
    m_name=m_name_entry

    _admn_no=Label(win_update,text='Admission No',font=('fenix',12))
    _name=Label(win_update,text='Name',font=('fenix',12))
    _dob=Label(win_update,text='DOB(YYYY-MM-DD)',font=('fenix',12))
    _contact=Label(win_update,text='Contact',font=('fenix',12))
    _f_name=Label(win_update,text='Father Name',font=('fenix',12))
    _m_name=Label(win_update,text='Mother Name',font=('fenix',12))

    upd_stu_b=Button(win_update,text='UPDATE',font=('Fenix',15),command=upd_stu)
    upd_stu_b_back=Button(win_update,text='Back',font=('Fenix',12),command=win_update.destroy)

    upd_can.create_window(80,30,window=_admn_no)
    upd_can.create_window(80,70,window=_name)
    upd_can.create_window(80,110,window=_dob)
    upd_can.create_window(80,150,window=_contact)
    upd_can.create_window(80,190,window=_f_name)
    upd_can.create_window(80,230,window=_m_name)

    upd_can.create_window(250,30,window=admn_no_entry)
    upd_can.create_window(250,110,window=dob_entry)
    upd_can.create_window(250,70,window=name_entry)
    upd_can.create_window(250,150,window=contact_entry)
    upd_can.create_window(250,190,window=f_name_entry)
    upd_can.create_window(250,230,window=m_name_entry)

    upd_can.create_window(200,330,window=upd_stu_b)
    upd_can.create_window(200,380,window=upd_stu_b_back)

    win_update.mainloop()

def upd_stu():
    admn_no_info=(admn_no.get()).lower()
    name_info=(name.get()).lower()
    dob_info=(dob.get()).lower()
    contact_info=(contact.get()).lower()
    f_name_info=(f_name.get()).lower()
    m_name_info=(m_name.get()).lower()
    if len(admn_no_info)==0 or len(name_info)==0 or len(dob_info)==0 or len(contact_info)==0 or len(f_name_info)==0 or len(m_name_info)==0:
        tkinter.messagebox.showerror('Empty','Filing all fields is mandatory!')
    else:
        mycursor.execute("update students set admn_no='%s',name='%s',dob='%s',contact='%s',father_name='%s',mother_name='%s' where admn_no='%s'"%(admn_no_info,name_info,dob_info,contact_info,f_name_info,m_name_info,admn_no_info))
        mydb.commit()
        admn_no_entry.delete(0,END)
        name_entry.delete(0,END)
        dob_entry.delete(0,END)
        contact_entry.delete(0,END)
        f_name_entry.delete(0,END)
        m_name_entry.delete(0,END)
        tkinter.messagebox.showinfo('Success','Successfully updated student details in the database!')
        teacher('')

def t_delstudent():
    windels=Toplevel(t_screen)
    windels.title('Delete Student')
    global admission_no
    admission_no=StringVar()
    l1=Label(windels,text='Admission No')
    e1=Entry(windels,textvariable=admission_no)
    admission_no=e1
    b1=Button(windels,text='DELETE',command=deletestudent)
    b2=Button(windels,text='Back',command=windels.destroy)
    l1.grid(column=0,row=0)
    e1.grid(column=1,row=0)
    b1.grid(column=0,row=1)
    b2.grid(column=1,row=1)
    
def deletestudent():
    k_adm_no=admission_no.get()
    try:
        mycursor.execute(f'delete from students where admn_no={k_adm_no}')
        m=tkinter.messagebox.showinfo('Success','Success !')
        mydb.commit()
        teacher('')
    except Exception as e:
        m=tkinter.messagebox.showerror('Error !',e)

#   Dashboard - Admin
def admin():
    try:
        screen_login.destroy()
        screen.destroy()
    except:
        pass

    global adm_screen
    adm_screen=Tk()
    adm_screen.geometry('300x200')
    adm_screen.title('Admin\'s DashBoard')
    try:
        adm_screen.deiconify()
    except:
        pass

    global adm_can
    adm_can=Canvas(adm_screen,width=300,height=200)
    img=PhotoImage(file='ppm/adminbg.ppm')
    image=adm_can.create_image(0,0,anchor=NW,image=img)
    adm_can.pack()

    adm_t=Button(adm_screen,text='Teacher\'s Data',font=('fenix',20),command=teacher_data)
    adm_s=Button(adm_screen,text='Student\'s Data',font=('fenix',20),command=student_data)

    adm_can.create_window(150,50,window=adm_t)
    adm_can.create_window(150,130,window=adm_s)
    adm_screen.mainloop()

def teacher_data():
    global t_d_screen
    try:
        t_d_screen.destroy()
    except:
        pass
    
    t_d_screen=Toplevel(adm_screen)
    t_d_screen.geometry('900x600')
   
    try:
        adm_screen.iconify()
    except:
        pass

    global td_can
    td_can=Canvas(t_d_screen,width=900,height=600)
    img=PhotoImage(file='ppm/t_d_bg.ppm')
    image =td_can.create_image(0,0,anchor=NW,image=img)
    td_can.pack()

    #search bar
    global sea
    sea=StringVar()
    a_search=Button(t_d_screen,
                    text='Search',
                    font=('fenix',12),
                    command=search_tea)
    sea_entry=Entry(t_d_screen,
                    textvariable=sea,
                    font=('Fenix',13))
    sea_entry.pack()
    sea=sea_entry
    _sea=Label(t_d_screen,text='Search by Name',font=('fenix',11))

    display_teacher()

    #add teacher
    t_d_add=Button(t_d_screen,text='Add Teacher',font=('fenix',13),command=t_addteacher)
    # update student
    t_d_upd=Button(t_d_screen,text='Update',font=('fenix',13),command=lambda:t_updateteacher(''))
    # Delete teacher
    t_d_del=Button(t_d_screen,text='Delete Teacher',font=('fenix',13),command=td_delteacher)
    # Exit
    t_d_b=Button(t_d_screen,text='Back',font=('fenix',13),command=back_and_deicon2)
    # Hint label
    l_upd=Label(t_d_screen,text='You can double click to EDIT/UPDATE any entry.')
    
    #placing everything
    td_can.create_window(245,30,window=a_search)
    td_can.create_window(110,30,window=sea_entry)
    td_can.create_window(110,55,window=_sea)
    td_can.create_window(490,30,window=t_d_b)
    td_can.create_window(680,30,window=t_d_del)
    td_can.create_window(820,30,window=t_d_add)
    td_can.create_window(560,30,window=t_d_upd)
    td_can.create_window(530,60,window=l_upd)
    t_d_screen.mainloop()

def display_teacher(): 
    # Displays records in tabular form, written separately to ease ediions
    table_frame=Frame(t_d_screen,bd=4,relief=RIDGE,bg='azure')
    table_frame.place(x=10,y=70,width=875,height=520)
          
    scroll_x=Scrollbar(table_frame,orient=HORIZONTAL)
    scroll_y=Scrollbar(table_frame,orient=VERTICAL)

    global teacher_table
    teacher_table=ttk.Treeview(table_frame,columns=('t_no','name','dob','contact','f_name','m_name'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

    scroll_x.pack(side=BOTTOM,fill=X)
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_x.config(command=teacher_table.xview)
    scroll_y.config(command=teacher_table.yview)
    
    teacher_table.heading('t_no',text='Teacher No')
    teacher_table.heading('name',text='Name')
    teacher_table.heading('dob',text='DOB')
    teacher_table.heading('contact',text='Contact No')
    teacher_table.heading('f_name',text='Father\'s Name')
    teacher_table.heading('m_name',text='Mother\'s name')
    teacher_table['show']='headings'  # To hide first column of index of data (metadata)
    teacher_table.column('t_no',width=110)
    teacher_table.column('name',width=150)
    teacher_table.column('dob',width=130)
    teacher_table.column('contact',width=150)
    teacher_table.column('f_name',width=150)
    teacher_table.column('m_name',width=150)
    teacher_table.pack(fill=BOTH,expand=1)
    teacher_table.bind('<Double-Button-1>',t_updateteacher)
    fetch_table_data_t()

def fetch_table_data_t():
    mycursor.execute('select * from teachers order by t_no')
    rows=mycursor.fetchall()
    global teacher_table
    if rows!=0:
        try:
            teacher_table.delete(teacher_table.get_children())
        except :
            pass
        for row in rows:
            teacher_table.insert('',END,values=row)

def t_addteacher():
    t_d_screen.iconify()
    global addt_screen
    addt_screen=Toplevel(t_d_screen)
    addt_screen.geometry('400x400')
    addt_screen.title('Add Teacher')

    global add_student_a_can
    addt_can=Canvas(addt_screen,width=400,height=400)
    img=PhotoImage(file='ppm/addbg.ppm')
    image=addt_can.create_image(-200,0,anchor=NW,image=img)
    addt_can.pack()

    global t_no
    global name1
    global dob1
    global contact1
    global f_name1
    global m_name1

    t_no = StringVar()
    name1=StringVar()
    dob1=StringVar()
    contact1=StringVar()
    f_name1=StringVar()
    m_name1=StringVar()

    global t_no_entry
    global name_entry1
    global dob_entry1
    global contact_entry1
    global f_name_entry1
    global m_name_entry1

    t_no_entry=Entry(addt_screen,textvariable='t_no',font=('Fenix',12))
    name_entry1=Entry(addt_screen,textvariable='name1',font=('Fenix',12))
    dob_entry1=Entry(addt_screen,textvariable='dob1',font=('Fenix',12))
    contact_entry1=Entry(addt_screen,textvariable='contact1',font=('Fenix',12))
    f_name_entry1=Entry(addt_screen,textvariable='f_name1',font=('Fenix',12))
    m_name_entry1=Entry(addt_screen,textvariable='m_name1',font=('Fenix',12))

    t_no_entry.delete(0,END)

    t_no=t_no_entry
    name1=name_entry1
    dob1=dob_entry1
    contact1=contact_entry1
    f_name1=f_name_entry1
    m_name1=m_name_entry1

    _t_no=Label(addt_screen,text='Teacher No',font=('fenix',12))
    _name1=Label(addt_screen,text='Name',font=('fenix',12))
    _dob1=Label(addt_screen,text='DOB(YYYY-MM-DD)',font=('fenix',12))
    _contact1=Label(addt_screen,text='Contact',font=('fenix',12))
    _f_name1=Label(addt_screen,text='Father Name',font=('fenix',12))
    _m_name1=Label(addt_screen,text='Mother Name',font=('fenix',12))

    add_stu_b1=Button(addt_screen,text='Add Teacher',font=('Fenix',15),command=add_tea)
    add_stu_b_back1=Button(addt_screen,text='Back',font=('Fenix',12),command=back_addt_to_adminDash)

    addt_can.create_window(80,30,window=_t_no)
    addt_can.create_window(80,70,window=_name1)
    addt_can.create_window(80,110,window=_dob1)
    addt_can.create_window(80,150,window=_contact1)
    addt_can.create_window(80,190,window=_f_name1)
    addt_can.create_window(80,230,window=_m_name1)

    addt_can.create_window(250,30,window=t_no_entry)
    addt_can.create_window(250,110,window=dob_entry1)
    addt_can.create_window(250,70,window=name_entry1)
    addt_can.create_window(250,150,window=contact_entry1)
    addt_can.create_window(250,190,window=f_name_entry1)
    addt_can.create_window(250,230,window=m_name_entry1)

    addt_can.create_window(200,330,window=add_stu_b1)
    addt_can.create_window(200,380,window=add_stu_b_back1)

    addt_screen.mainloop()

def t_updateteacher(ev):
    cursor_row=teacher_table.focus()
    content=teacher_table.item(cursor_row)
    row=content['values']
    if len(cursor_row)==0:
        msgbx.showerror('Error','No Record selected')
        return
    global win_update
    win_update=Toplevel(t_d_screen)
    win_update.title('Update Details')
    win_update.geometry('400x400')

    global upd_can
    upd_can=Canvas(win_update,width=400,height=400)
    img=PhotoImage(file='ppm/addbg.ppm')
    image=upd_can.create_image(-200,0,anchor=NW,image=img)
    upd_can.pack()

    global t_no
    global name2
    global dob2
    global contact2
    global f_name2
    global m_name2

    t_no = StringVar()
    name2=StringVar()
    dob2=StringVar()
    contact2=StringVar()
    f_name2=StringVar()
    m_name2=StringVar()

    global t_no_entry
    global name_entry2
    global dob_entry2
    global contact_entry2
    global f_name_entry2
    global m_name_entry2

    t_no_entry=Entry(win_update,textvariable='t_no',font=('Fenix',12))
    name_entry2=Entry(win_update,textvariable='name',font=('Fenix',12))
    dob_entry2=Entry(win_update,textvariable='dob',font=('Fenix',12))
    contact_entry2=Entry(win_update,textvariable='contact',font=('Fenix',12))
    f_name_entry2=Entry(win_update,textvariable='f_name',font=('Fenix',12))
    m_name_entry2=Entry(win_update,textvariable='m_name',font=('Fenix',12))
    
    t_no_entry.delete(0,END)
    name_entry2.delete(0,END)
    dob_entry2.delete(0,END)
    contact_entry2.delete(0,END)
    f_name_entry2.delete(0,END)
    m_name_entry2.delete(0,END)

    t_no_entry.insert(0,row[0])
    name_entry2.insert(0,row[1])
    dob_entry2.insert(0,row[2])
    contact_entry2.insert(0,row[3])
    f_name_entry2.insert(0,row[4])
    m_name_entry2.insert(0,row[5])

    t_no=t_no_entry
    name2=name_entry2
    dob2=dob_entry2
    contact2=contact_entry2
    f_name2=f_name_entry2
    m_name2=m_name_entry2

    _t_no=Label(win_update,text='Teacher No',font=('fenix',12))
    _name=Label(win_update,text='Name',font=('fenix',12))
    _dob=Label(win_update,text='DOB(YYYY-MM-DD)',font=('fenix',12))
    _contact=Label(win_update,text='Contact',font=('fenix',12))
    _f_name=Label(win_update,text='Father Name',font=('fenix',12))
    _m_name=Label(win_update,text='Mother Name',font=('fenix',12))

    upd_tea_b=Button(win_update,text='UPDATE',font=('Fenix',15),command=upd_tea)
    upd_tea_b_back=Button(win_update,text='Back',font=('Fenix',12),command=win_update.destroy)

    upd_can.create_window(80,30,window=_t_no)
    upd_can.create_window(80,70,window=_name)
    upd_can.create_window(80,110,window=_dob)
    upd_can.create_window(80,150,window=_contact)
    upd_can.create_window(80,190,window=_f_name)
    upd_can.create_window(80,230,window=_m_name)

    upd_can.create_window(250,30,window=t_no_entry)
    upd_can.create_window(250,110,window=dob_entry2)
    upd_can.create_window(250,70,window=name_entry2)
    upd_can.create_window(250,150,window=contact_entry2)
    upd_can.create_window(250,190,window=f_name_entry2)
    upd_can.create_window(250,230,window=m_name_entry2)

    upd_can.create_window(200,330,window=upd_tea_b)
    upd_can.create_window(200,380,window=upd_tea_b_back)

    win_update.mainloop()

def upd_tea():
    t_no_info=(t_no.get()).lower()
    name_info=(name2.get()).lower()
    dob_info=(dob2.get()).lower()
    contact_info=(contact2.get()).lower()
    f_name_info=(f_name2.get()).lower()
    m_name_info=(m_name2.get()).lower()
    if len(t_no_info)==0 or len(name_info)==0 or len(dob_info)==0 or len(contact_info)==0 or len(f_name_info)==0 or len(m_name_info)==0:
        tkinter.messagebox.showerror('Empty','Filing all fields is mandatory!')
    else:
        mycursor.execute("update teachers set t_no='%s',name='%s',dob='%s',contact='%s',father_name='%s',mother_name='%s' where t_no='%s'"%(t_no_info,name_info,dob_info,contact_info,f_name_info,m_name_info,t_no_info))
        mydb.commit()
        t_no_entry.delete(0,END)
        name_entry2.delete(0,END)
        dob_entry2.delete(0,END)
        contact_entry2.delete(0,END)
        f_name_entry2.delete(0,END)
        m_name_entry2.delete(0,END)
        tkinter.messagebox.showinfo('Success','Successfully updated student details in the database!')
        t_d_screen.destroy()
        teacher_data()

def search_tea():
    search_info=(sea.get()).lower()
    mycursor.execute('select * from teachers where name=\'%s\''%search_info)
    result=mycursor.fetchall()
    if len(result)==0:
        tkinter.messagebox.showerror('Not Found','No Teacher found!')
    else:
        search_display_t(result)

def td_delteacher():
    windels=Toplevel(t_d_screen)
    windels.title('DELETE TEACHER')
    global teacher_no
    teacher_no=StringVar()
    l1=Label(windels,text='Teacher No')
    e1=Entry(windels,textvariable=teacher_no)
    teacher_no=e1
    b1=Button(windels,text='DELETE',command=deleteteacher)
    b2=Button(windels,text='Back',command=windels.destroy)
    l1.grid(column=0,row=0)
    e1.grid(column=1,row=0)
    b1.grid(column=0,row=1)
    b2.grid(column=1,row=1)
    
def deleteteacher():
    k_teacher_no=teacher_no.get()
    try:
        mycursor.execute(f'delete from teachers where t_no={k_teacher_no}')
        m=tkinter.messagebox.showinfo('Success','Success !')
        mydb.commit()
        teacher_data()
    except Exception as e:
        m=tkinter.messagebox.showerror('Error !',e)
    pass

def add_tea():
    t_no_info=(t_no.get()).lower()
    name_info1=(name1.get()).lower()
    dob_info1=(dob1.get()).lower()
    contact_info1=(contact1.get()).lower()
    f_name_info1=(f_name1.get()).lower()
    m_name_info1=(m_name1.get()).lower()
    if len(t_no_info)==0 or len(name_info1)==0 or len(dob_info1)==0 or len(contact_info1)==0 or len(f_name_info1)==0 or len(m_name_info1)==0:
        tkinter.messagebox.showerror('Empty','Filing all fields is mandatory!')
    else:
        mycursor.execute("insert into teachers value('%s','%s','%s','%s','%s','%s')"%(t_no_info,name_info1,dob_info1,contact_info1,f_name_info1,m_name_info1))
        mydb.commit()
        t_no_entry.delete(0,END)
        name_entry1.delete(0,END)
        dob_entry1.delete(0,END)
        contact_entry1.delete(0,END)
        f_name_entry1.delete(0,END)
        m_name_entry1.delete(0,END)
        tkinter.messagebox.showinfo('Success','Successfully added teacher to the database!')
        teacher_data()

#   Admin Student data
def student_data():
    global t_s_screen
    try:
        t_s_screen.destroy()
    except:
        pass

    t_s_screen=Toplevel(adm_screen)
    t_s_screen.geometry('900x600')
    t_s_screen.title('Admin DB - Student Data')
   
    try:
        adm_screen.iconify()
    except:
        pass

    global ts_can
    ts_can=Canvas(t_s_screen,width=900,height=600)
    img=PhotoImage(file='ppm/t_d_bg.ppm')
    image =ts_can.create_image(0,0,anchor=NW,image=img)
    ts_can.pack()

    #search bar
    global se
    se=StringVar()
    a_search=Button(t_s_screen,
                    text='Search',
                    font=('fenix',12),
                    command=search_stu)
    se_entry=Entry(t_s_screen,
                    textvariable=se,
                    font=('Fenix',13))
    se_entry.pack()
    se=se_entry
    _se_a=Label(t_s_screen,text='Search by Name',font=('fenix',11))

    display_student_a()

    #add student
    t_s_add=Button(t_s_screen,text='Add Student',font=('fenix',13),command=t_addstudent_a)
    # update student
    t_s_upd=Button(t_s_screen,text='Update',font=('fenix',13),command=lambda:t_updatestudent_a(''))
    # Delete student
    t_s_del=Button(t_s_screen,text='Delete Student',font=('fenix',13),command=t_delstudent_a)
    # back
    t_s_b=Button(t_s_screen,text='Back',font=('fenix',13),command=back_and_deicon3)
    # Hint label
    l_upd=Label(t_s_screen,text='You can double click to EDIT/UPDATE any entry.')

    #placing everything
    ts_can.create_window(245,30,window=a_search)
    ts_can.create_window(110,30,window=se_entry)
    ts_can.create_window(110,55,window=_se_a)
    ts_can.create_window(490,30,window=t_s_b)
    ts_can.create_window(680,30,window=t_s_del)
    ts_can.create_window(820,30,window=t_s_add)
    ts_can.create_window(560,30,window=t_s_upd)
    ts_can.create_window(530,60,window=l_upd)
    t_s_screen.mainloop()

def display_student_a(): 
    # Displays records in tabular form, written separately to ease ediions
    table_frame=Frame(t_s_screen,bd=4,relief=RIDGE,bg='azure')
    table_frame.place(x=10,y=70,width=875,height=520)
          
    scroll_x=Scrollbar(table_frame,orient=HORIZONTAL)
    scroll_y=Scrollbar(table_frame,orient=VERTICAL)

    global student_table_a
    student_table_a=ttk.Treeview(table_frame,columns=('admn_no','name','dob','contact','f_name','m_name'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

    scroll_x.pack(side=BOTTOM,fill=X)
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_x.config(command=student_table_a.xview)
    scroll_y.config(command=student_table_a.yview)
    
    student_table_a.heading('admn_no',text='Admission No')
    student_table_a.heading('name',text='Name')
    student_table_a.heading('dob',text='DOB')
    student_table_a.heading('contact',text='Contact No')
    student_table_a.heading('f_name',text='Father\'s Name')
    student_table_a.heading('m_name',text='Mother\'s name')
    student_table_a['show']='headings'  # To hide first column of index of data (metadata)
    student_table_a.column('admn_no',width=110)
    student_table_a.column('name',width=150)
    student_table_a.column('dob',width=130)
    student_table_a.column('contact',width=150)
    student_table_a.column('f_name',width=150)
    student_table_a.column('m_name',width=150)
    student_table_a.pack(fill=BOTH,expand=1)
    student_table_a.bind('<Double-Button-1>',t_updatestudent_a)
    fetch_table_data_s_a()

def fetch_table_data_s_a():
    mycursor.execute('select * from students order by admn_no')
    rows=mycursor.fetchall()
    global student_table_a
    if rows!=0:
        try:
            student_table_a.delete(student_table_a.get_children())
        except :
            pass
        for row in rows:
            student_table_a.insert('',END,values=row)

def t_addstudent_a():
    t_s_screen.iconify()
    global add_student_a_screen
    add_student_a_screen=Toplevel(t_s_screen)
    add_student_a_screen.geometry('400x400')
    add_student_a_screen.title('Add Student')

    global add_student_a_can
    add_student_a_can=Canvas(add_student_a_screen,width=400,height=400)
    img=PhotoImage(file='ppm/addbg.ppm')
    image=add_student_a_can.create_image(-200,0,anchor=NW,image=img)
    add_student_a_can.pack()

    global admn_no
    global name
    global dob
    global contact
    global f_name
    global m_name
    global admn_no_entry
    global name_entry
    global dob_entry
    global contact_entry
    global f_name_entry
    global m_name_entry

    admn_no = StringVar()
    name=StringVar()
    dob=StringVar()
    contact=StringVar()
    f_name=StringVar()
    m_name=StringVar()

    admn_no_entry=Entry(add_student_a_screen,textvariable='admn_no',font=('Fenix',12))
    name_entry=Entry(add_student_a_screen,textvariable='name',font=('Fenix',12))
    dob_entry=Entry(add_student_a_screen,textvariable='dob',font=('Fenix',12))
    contact_entry=Entry(add_student_a_screen,textvariable='contact',font=('Fenix',12))
    f_name_entry=Entry(add_student_a_screen,textvariable='f_name',font=('Fenix',12))
    m_name_entry=Entry(add_student_a_screen,textvariable='m_name',font=('Fenix',12))

    admn_no_entry.delete(0,END)
    name_entry.delete(0,END)
    dob_entry.delete(0,END)
    contact_entry.delete(0,END)
    f_name_entry.delete(0,END)
    m_name_entry.delete(0,END)

    admn_no=admn_no_entry
    name=name_entry
    dob=dob_entry
    contact=contact_entry
    f_name=f_name_entry
    m_name=m_name_entry

    _admn_no=Label(add_student_a_screen,text='Admission No',font=('fenix',12))
    _name=Label(add_student_a_screen,text='Name',font=('fenix',12))
    _dob=Label(add_student_a_screen,text='DOB(YYYY-MM-DD)',font=('fenix',12))
    _contact=Label(add_student_a_screen,text='Contact',font=('fenix',12))
    _f_name=Label(add_student_a_screen,text='Father Name',font=('fenix',12))
    _m_name=Label(add_student_a_screen,text='Mother Name',font=('fenix',12))

    add_stu_b=Button(add_student_a_screen,text='Add Student',font=('Fenix',15),command=add_stu_a)
    add_stu_b_back=Button(add_student_a_screen,text='Back',font=('Fenix',12),command=back_and_deicon4)

    add_student_a_can.create_window(80,30,window=_admn_no)
    add_student_a_can.create_window(80,70,window=_name)
    add_student_a_can.create_window(80,110,window=_dob)
    add_student_a_can.create_window(80,150,window=_contact)
    add_student_a_can.create_window(80,190,window=_f_name)
    add_student_a_can.create_window(80,230,window=_m_name)

    add_student_a_can.create_window(250,30,window=admn_no_entry)
    add_student_a_can.create_window(250,110,window=dob_entry)
    add_student_a_can.create_window(250,70,window=name_entry)
    add_student_a_can.create_window(250,150,window=contact_entry)
    add_student_a_can.create_window(250,190,window=f_name_entry)
    add_student_a_can.create_window(250,230,window=m_name_entry)

    add_student_a_can.create_window(200,330,window=add_stu_b)
    add_student_a_can.create_window(200,380,window=add_stu_b_back)

    add_student_a_screen.mainloop()

def t_updatestudent_a(ev):
    cursor_row=student_table_a.focus()
    content=student_table_a.item(cursor_row)
    row=content['values']

    if len(cursor_row)==0:
        msgbx.showerror('Error','No Record selected')
        return
    
    global win_update
    win_update=Toplevel(t_s_screen)
    win_update.title('Update Details')
    win_update.geometry('400x400')

    global upd_can
    upd_can=Canvas(win_update,width=400,height=400)
    img=PhotoImage(file='ppm/addbg.ppm')
    image=upd_can.create_image(-200,0,anchor=NW,image=img)
    upd_can.pack()

    global admn_no
    global name
    global dob
    global contact
    global f_name
    global m_name

    admn_no=name=dob=contact=f_name=m_name=''

    admn_no = StringVar()
    name=StringVar()
    dob=StringVar()
    contact=StringVar()
    f_name=StringVar()
    m_name=StringVar()

    global admn_no_entry
    global name_entry
    global dob_entry
    global contact_entry
    global f_name_entry
    global m_name_entry
    
    admn_no_entry=Entry(win_update,textvariable='admn_no',font=('Fenix',12))
    name_entry=Entry(win_update,textvariable='name',font=('Fenix',12))
    dob_entry=Entry(win_update,textvariable='dob',font=('Fenix',12))
    contact_entry=Entry(win_update,textvariable='contact',font=('Fenix',12))
    f_name_entry=Entry(win_update,textvariable='f_name',font=('Fenix',12))
    m_name_entry=Entry(win_update,textvariable='m_name',font=('Fenix',12))

    admn_no_entry.delete(0,END)
    name_entry.delete(0,END)
    dob_entry.delete(0,END)
    contact_entry.delete(0,END)
    f_name_entry.delete(0,END)
    m_name_entry.delete(0,END)
    
    admn_no_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    dob_entry.insert(0,row[2])
    contact_entry.insert(0,row[3])
    f_name_entry.insert(0,row[4])
    m_name_entry.insert(0,row[5])
    
    admn_no=admn_no_entry
    name=name_entry
    dob=dob_entry
    contact=contact_entry
    f_name=f_name_entry
    m_name=m_name_entry

    _admn_no=Label(win_update,text='Admission No',font=('fenix',12))
    _name=Label(win_update,text='Name',font=('fenix',12))
    _dob=Label(win_update,text='DOB(YYYY-MM-DD)',font=('fenix',12))
    _contact=Label(win_update,text='Contact',font=('fenix',12))
    _f_name=Label(win_update,text='Father Name',font=('fenix',12))
    _m_name=Label(win_update,text='Mother Name',font=('fenix',12))

    upd_stu_b=Button(win_update,text='UPDATE',font=('Fenix',15),command=upd_stu_a)
    upd_stu_b_back=Button(win_update,text='Back',font=('Fenix',12),command=win_update.destroy)

    upd_can.create_window(80,30,window=_admn_no)
    upd_can.create_window(80,70,window=_name)
    upd_can.create_window(80,110,window=_dob)
    upd_can.create_window(80,150,window=_contact)
    upd_can.create_window(80,190,window=_f_name)
    upd_can.create_window(80,230,window=_m_name)

    upd_can.create_window(250,30,window=admn_no_entry)
    upd_can.create_window(250,110,window=dob_entry)
    upd_can.create_window(250,70,window=name_entry)
    upd_can.create_window(250,150,window=contact_entry)
    upd_can.create_window(250,190,window=f_name_entry)
    upd_can.create_window(250,230,window=m_name_entry)

    upd_can.create_window(200,330,window=upd_stu_b)
    upd_can.create_window(200,380,window=upd_stu_b_back)

    win_update.mainloop()

def upd_stu_a():
    admn_no_info=(admn_no.get()).lower()
    name_info=(name.get()).lower()
    dob_info=(dob.get()).lower()
    contact_info=(contact.get()).lower()
    f_name_info=(f_name.get()).lower()
    m_name_info=(m_name.get()).lower()
    if len(admn_no_info)==0 or len(name_info)==0 or len(dob_info)==0 or len(contact_info)==0 or len(f_name_info)==0 or len(m_name_info)==0:
        tkinter.messagebox.showerror('Empty','Filing all fields is mandatory!')
    else:
        mycursor.execute("update students set admn_no='%s',name='%s',dob='%s',contact='%s',father_name='%s',mother_name='%s' where admn_no='%s'"%(admn_no_info,name_info,dob_info,contact_info,f_name_info,m_name_info,admn_no_info))
        mydb.commit()
        admn_no_entry.delete(0,END)
        name_entry.delete(0,END)
        dob_entry.delete(0,END)
        contact_entry.delete(0,END)
        f_name_entry.delete(0,END)
        m_name_entry.delete(0,END)
        tkinter.messagebox.showinfo('Success','Successfully updated student details in the database!')
        student_data()

def t_delstudent_a():
    windels=Toplevel(t_s_screen)
    windels.title('Delete Student')
    global admission_no
    admission_no=StringVar()
    l1=Label(windels,text='Admission No')
    e1=Entry(windels,textvariable=admission_no)
    admission_no=e1
    b1=Button(windels,text='DELETE',command=deletestudent_a)
    b2=Button(windels,text='Back',command=windels.destroy)
    l1.grid(column=0,row=0)
    e1.grid(column=1,row=0)
    b1.grid(column=0,row=1)
    b2.grid(column=1,row=1)
    
def deletestudent_a():
    k_adm_no=admission_no.get()
    try:
        mycursor.execute(f'delete from students where admn_no={k_adm_no}')
        m=tkinter.messagebox.showinfo('Success','Success !')
        mydb.commit()
        student_data()
    except Exception as e:
        m=tkinter.messagebox.showerror('Error !',e)

def add_stu_a():
    admn_no_info=(admn_no.get()).lower()
    name_info=(name.get()).lower()
    dob_info=(dob.get()).lower()
    contact_info=(contact.get()).lower()
    f_name_info=(f_name.get()).lower()
    m_name_info=(m_name.get()).lower()
    if len(admn_no_info)==0 or len(name_info)==0 or len(dob_info)==0 or len(contact_info)==0 or len(f_name_info)==0 or len(m_name_info)==0:
        tkinter.messagebox.showerror('Empty','Filing all fields is mandatory!')
    else:
        mycursor.execute("insert into students value('%s','%s','%s','%s','%s','%s')"%(admn_no_info,name_info,dob_info,contact_info,f_name_info,m_name_info))
        mydb.commit()
        admn_no_entry.delete(0,END)
        name_entry.delete(0,END)
        dob_entry.delete(0,END)
        contact_entry.delete(0,END)
        f_name_entry.delete(0,END)
        m_name_entry.delete(0,END)
        tkinter.messagebox.showinfo('Success','Successfully added student to the database!')
        student_data()

def search_display_s(result):
    s='  |  '
    dat=f'Admn No{s}Name{s}DOB{s}Contact No{s}FName{s}MName'
    dat+='\n'+'-'*65+'\n'
    for i in result:
        for j in i:
            dat+=str(j)+'  |  '
        dat+='\n'
    msgbx.showinfo('Found !',dat)

def search_display_t(result):
    s='  |  '
    dat=f'Teacher No{s}Name{s}DOB{s}Contact No{s}FName{s}MName'
    dat+='\n'+'-'*67+'\n'
    for i in result:
        for j in i:
            dat+=str(j)+'  |  '
        dat+='\n'
    msgbx.showinfo('Found !',dat)

#   back from Login/Register to info screen
def back_to_screen(screen_name):
    screen_name.destroy()
    screen.wm_state('normal')
    
# back from add teacher to admin db
def back_addt_to_adminDash():
    addt_screen.destroy()
    t_d_screen.deiconify()
    
# exit with warning
def exit_pro():
    w=tkinter.messagebox.askyesno(title='Exiting?',message='Do you really want to exit ?')
    if w==True:
        exit()

#   Will be removed and replaced by quit()
def back_dash_to_welcome():
    dash.destroy()
    welcome()

welcome()
