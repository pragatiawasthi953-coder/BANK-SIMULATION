from tkinter import Tk,Label,Frame,Button,Entry,messagebox,simpledialog
import time
import table_creator
table_creator.create()
from datetime import datetime
import generator
import sqlite3
import Email_handler
import re
from PIL import Image,ImageTk

def update_time():
    curdate=time.strftime("%d-%b-%Y [TIME] %I:%M:%S %p")
    date.configure(text=curdate)
    date.after(1000,update_time)

def main_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2) 
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.13,relwidth=0.5,relheight=.8)  

    
    

root=Tk()
root.state('zoomed')
root.resizable(width=False,height=False)
root.configure(bg="light green")
title=Label(root,text='BANKING SIMULATION',font=('arial',40,'bold','underline'),bg='light green')
title.pack()

curdate=time.strftime("%d-%b-%Y [TIME] %I:%M:%S %p")
date=Label(root,text=curdate,font=('arial',18,'bold'),bg='light green',fg='red')
date.pack(pady=10)
update_time()

img=Image.open(r"C:\Users\user\Downloads\logo.jpg").resize((185,110))
imgtk=ImageTk.PhotoImage(img,master=root)

lbl_img=Label(root,image=imgtk)
lbl_img.place(relx=0.001,rely=0)

img2=Image.open(r"C:\Users\user\Downloads\logo2.jpg").resize((200,130))
imgtk2=ImageTk.PhotoImage(img2,master=root)

lbl_img2=Label(root,image=imgtk2)
lbl_img2.place(relx=.86,rely=0)


footer=Label(root,text='Developed by Pragati Awasthi',font=('arial',20,'bold'),bg='light green')
footer.pack(side='bottom')

def forgot_screen():
    def back():
        frm.destroy()
        existuser_screen()
 
    def send_otp():
        gen_otp=generator.generate_otp()
        acn=e_acn.get()
        adhar=e_adhar.get()
        
        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select name,email,pass from accounts where acn=? and adhar=?'''
        curobj.execute(query,(acn,adhar))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('Forgot Password','Record not found')
        else:
            Email_handler.send_otp(tup[1],tup[0],gen_otp)
            user_otp=simpledialog.askinteger("Password Recovery","Enter OTP")
            if gen_otp==user_otp:
                messagebox.showinfo("Password Recovery",f"Your Password = {tup[2]}")
            else:
                messagebox.showerror("Password Recovery","Invalid otp")   


    frm = Frame(root, highlightbackground='black', highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.15, relwidth=1, relheight=.8)

    back_button=Button(frm,text='BACK',bg='light green',font=('calibri',18,'bold'),bd=5,command=back)
    back_button.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='💳ACN_NO',font=('calibri',20,'bold'),bg='green',fg='black',width=10)
    lbl_acn.place(relx=.3,rely=.25)

    e_acn=Entry(frm,font=('calibri',20,'bold'),bd=5)
    e_acn.place(relx=.43,rely=.25)
    e_acn.focus()

    lbl_adhar=Label(frm,text='📄Adhar',font=('calibri',20,'bold'),bg='green',fg='black',width=10)
    lbl_adhar.place(relx=.3,rely=.35)

    e_adhar=Entry(frm,font=('calibri',20,'bold'),bd=5)
    e_adhar.place(relx=.43,rely=.35)

    otp_button=Button(frm,text='SEND_OTP',bg='light green',width=8,font=('calibri',18,'bold'),bd=5,command=send_otp)
    otp_button.place(relx=.37,rely=.5)

    reset_button=Button(frm,text='RESET',bg='light green',width=8,font=('calibri',18,'bold'),bd=5,command=back)
    reset_button.place(relx=.5,rely=.5)



def welcome_screen(acn=None):
    def logout():
        frm.destroy()
        main_screen()
    
    def check_screen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.11,relwidth=.7,relheight=.68)

        title_lbl=Label(ifrm,text='This screen displays registered account details',font=('calibri',20,'bold'),bg='white',fg='red')
        title_lbl.pack()

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select acn,bal,adhar,email,opendate from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        details=f'''
Account Number  =   {tup[0]}\n
Account Balance =   Rs.{tup[1]}\n
Account Adhar   =   {tup[2]}\n
Registered Email =  {tup[3]}\n
Account Opendate =  {tup[4]}\n
'''

        lbl_details=Label(ifrm,text=details,bg='white',fg='blue',font=('calibri',15,'bold'),anchor='w',justify='left')
        lbl_details.place(relx=.05,rely=.15)

    def update_screen():
        def update_db():
            name=e_name.get()
            email=e_email.get()
            mob=e_mob.get()
            pwd=e_pass.get()

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''update accounts set name=?,email=?,mob=?,pass=? where acn=?'''
            curobj.execute(query,(name,email,mob,pwd,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Screen","Details updated successfully")
            welcome_screen(acn)



        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select name,email,mob,pass from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()
    
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.11,relwidth=.7,relheight=.68)

        title_lbl=Label(ifrm,text='This screen displays all the updated account details',font=('calibri',20,'bold'),bg='white',fg='red')
        title_lbl.pack()   

        lbl_name=Label(ifrm,text='Name',width=7,font=('arial',15,'bold'),bg='RED',fg='white')
        lbl_name.place(relx=.02,rely=.2)

        e_name=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_name.place(relx=.17,rely=.2)
        e_name.focus()

        lbl_pass=Label(ifrm,text='Pass',width=7,font=('arial',15,'bold'),bg='RED',fg='white')
        lbl_pass.place(relx=.02,rely=.4)

        e_pass=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_pass.place(relx=.17,rely=.4)


        lbl_mob=Label(ifrm,text='Mob',width=7,font=('arial',15,'bold'),bg='RED',fg='white')
        lbl_mob.place(relx=.5,rely=.2)

        e_mob=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_mob.place(relx=.65,rely=.2)

        lbl_email=Label(ifrm,text='Email',width=7,font=('arial',15,'bold'),bg='RED',fg='white')
        lbl_email.place(relx=.5,rely=.4)

        e_email=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_email.place(relx=.65,rely=.4)

        e_name.insert(0,tup[0])
        e_email.insert(0,tup[1])
        e_mob.insert(0,tup[2])
        e_pass.insert(0,tup[3])
        

        submit_btn=Button(ifrm,text='Submit',width=8,bg='light green',
                        font=('arial',18,'bold'),bd=5,command=update_db)
        submit_btn.place(relx=.36,rely=.65)

    def deposit_screen():
        def deposit_db():
           amt=float(e_amt.get())
           conobj=sqlite3.connect(database='mybank.sqlite')
           curobj=conobj.cursor()
           query='''update accounts set bal=bal+? where acn=?'''
           curobj.execute(query,(amt,acn))
           conobj.commit()
           conobj.close()
           messagebox.showinfo("Deposit Screen",f'{amt} deposited successfully')
           e_amt.delete(0,"end")
           e_amt.focus()

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.11,relwidth=.7,relheight=.68)

        title_lbl=Label(ifrm,text='This screen displays all the deposit amount details',font=('calibri',20,'bold'),bg='white',fg='red')
        title_lbl.pack()  

        lbl_amt=Label(ifrm,text='Amount',width=8,font=('calibri',21,'bold'),bg='Green',fg='white')
        lbl_amt.place(relx=.28,rely=.28)

        e_amt=Entry(ifrm,font=('calibri',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.28)
        e_amt.focus()
   
        submit_btn=Button(ifrm,text='Submit',width=8,bg='light green',
                        font=('arial',18,'bold'),bd=5,command=deposit_db)
        
        submit_btn.place(relx=.39,rely=.51)
    

    def withdraw_screen():
        def withdraw_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database='mybank.sqlite')          
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup[0]>=amt:
                gen_otp=generator.generate_otp()
                Email_handler.send_otp_withdraw(tup[1],tup[2],gen_otp,amt)
                user_otp=simpledialog.askinteger("Withdraw OTP","OTP")
                if gen_otp==user_otp:
                    conobj=sqlite3.connect(database='mybank.sqlite')          
                    curobj=conobj.cursor()
                    query='''update accounts set bal=bal-? where acn=?'''
                    curobj.execute(query,(amt,acn))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Withdraw Screen",f'{amt} withdrawn successfully')
                    e_amt.delete(0,"end")
                    e_amt.focus()
                else:
                    messagebox.showerror("Withdraw Sceen","Invalid otp")
                    submit_btn.configure(text="resend otp")
            else:
                messagebox.showwarning("Withdarw Screen",f"Insufficient Bal: {tup[0]}")

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.11,relwidth=.7,relheight=.68)

        title_lbl=Label(ifrm,text='This screen displays all the withdraw amount details',font=('calibri',20,'bold'),bg='white',fg='red')
        title_lbl.pack() 

        lbl_amt=Label(ifrm,text='Amount',width=7,font=('arial',20,'bold'),bg='purple',fg='white')
        lbl_amt.place(relx=.28,rely=.32)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.43,rely=.32)
        e_amt.focus()


        submit_btn=Button(ifrm,text='Submit',width=8,bg='light green',
                        font=('arial',18,'bold'),bd=5,command=withdraw_db)
        submit_btn.place(relx=.4,rely=.52)       

    def transfer_screen():
        def transfer_db():
            to_acn=int(e_to.get())
            amt=float(e_amt.get())

            conobj=sqlite3.connect(database='mybank.sqlite')          
            curobj=conobj.cursor()
            query='''select * from accounts where acn=?'''
            curobj.execute(query,(to_acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showerror("Transfer Screen","Invalid To ACN")
                return
            
            conobj=sqlite3.connect(database='mybank.sqlite')          
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()
            if tup[0]>=amt:
                gen_otp=generator.generate_otp()
                Email_handler.send_otp_transfer(tup[1],tup[2],gen_otp,amt,to_acn)
                user_otp=simpledialog.askinteger("transfer OTP","OTP")
                if gen_otp==user_otp:
                    conobj=sqlite3.connect(database='mybank.sqlite')          
                    curobj=conobj.cursor()
                    query1='''update accounts set bal=bal-? where acn=?'''
                    query2='''update accounts set bal=bal+? where acn=?'''
                    
                    curobj.execute(query1,(amt,acn))
                    curobj.execute(query2,(amt,to_acn))
                    
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Trransfer Screen",f'{amt} transfered successfully')
                    e_amt.delete(0,"end")
                    e_amt.focus()
                else:
                    messagebox.showerror("Transfer Sceen","Invalid otp")
                    submit_btn.configure(text="resend otp")
            else:
                messagebox.showwarning("Transfer Screen",f"Insufficient Bal: {tup[0]}")

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.11,relwidth=.7,relheight=.68)

        title_lbl=Label(ifrm,text='This screen displays all the transfer amount details',font=('calibri',20,'bold'),bg='white',fg='red')
        title_lbl.pack()   

        lbl_to=Label(ifrm,text='To ACN',width=7,font=('calibri',19,'bold'),bg='brown',fg='white')
        lbl_to.place(relx=.24,rely=.2)

        e_to=Entry(ifrm,font=('calibri',20,'bold'),bd=5)
        e_to.place(relx=.4,rely=.2)
        e_to.focus()

        lbl_amt=Label(ifrm,text='Amount',width=7,font=('calibri',19,'bold'),bg='brown',fg='white')
        lbl_amt.place(relx=.24,rely=.35)

        e_amt=Entry(ifrm,font=('calibri',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.35)
        

        submit_btn=Button(ifrm,text='Transfer Amount',width=14,bg='light green',
                        font=('calibri',18,'bold'),bd=5,command=transfer_db)
        
        submit_btn.place(relx=.24,rely=.56)     

        check_blnc_button=Button(ifrm,text='Check Balance',bg='light green',font=('calibri',18,'bold'),bd=5,width=14,command=check_screen)
        check_blnc_button.place(relx=.5,rely=.56)
          



    conobj=sqlite3.connect(database='mybank.sqlite')
    curobj=conobj.cursor()
    query='''select name from accounts where acn=?'''
    curobj.execute(query,(acn,))
    tup=curobj.fetchone()
    conobj.close()
      

    
        
    frm = Frame(root, highlightbackground='black', highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.15, relwidth=1, relheight=.8)
    
    logout_button=Button(frm,text='LOG OUT',bg='light green',font=('calibri',18,'bold'),bd=5,command=logout)
    logout_button.place(relx=0.89,rely=0)

    lbl_wel=Label(frm,text=f'Welcome,{tup[0]}',font=('calibri',20,'bold'),bg='Blue',fg='black',width=17)
    lbl_wel.place(relx=.01,rely=.01)

    check_button=Button(frm,text='CHECK DETAILS',bg='yellow',font=('calibri',18,'bold'),bd=5,width=17,command=check_screen)
    check_button.place(relx=.01,rely=.12)

    update_button=Button(frm,text='UPDATE DETAILS',bg='red',font=('calibri',18,'bold'),bd=5,width=17,command=update_screen)
    update_button.place(relx=.01,rely=.27)
    
    deposit_button=Button(frm,text='DEPOSIT AMOUNT',bg='green',font=('calibri',18,'bold'),bd=5,width=17,command=deposit_screen)
    deposit_button.place(relx=.01,rely=.42)

    withdraw_button=Button(frm,text='WITHDRAW AMOUNT',bg='purple',font=('calibri',18,'bold'),bd=5,width=17,command=withdraw_screen)
    withdraw_button.place(relx=.01,rely=.57)
    
    transfer_button=Button(frm,text='TRANSFER AMOUNT',bg='brown',font=('calibri',18,'bold'),bd=5,width=17,command=transfer_screen)
    transfer_button.place(relx=.01,rely=.72)




def existuser_screen():
    def back():
        frm.destroy()
        main_screen()

    def fp_click():
        frm.destroy()
        forgot_screen()
        
    def reset_click():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()

    def submit_click():
        acn=e_acn.get()
        pwd=e_pass.get()
        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select * from accounts where acn=? and pass=?'''
        curobj.execute(query,(acn,pwd))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("Login","Invalid Credentials")
        else:
            acn=tup[0]
            frm.destroy()
            welcome_screen(acn)

        
    frm = Frame(root, highlightbackground='black', highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.15, relwidth=1, relheight=.8)

    back_button=Button(frm,text='BACK',bg='light green',font=('calibri',18,'bold'),bd=5,command=back)
    back_button.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='💳ACN_NO',font=('calibri',20,'bold'),bg='green',fg='black',width=10)
    lbl_acn.place(relx=.3,rely=.25)

    e_acn=Entry(frm,font=('calibri',20,'bold'),bd=5)
    e_acn.place(relx=.43,rely=.25)
    e_acn.focus()

    lbl_pass=Label(frm,text='🔒Password',font=('calibri',20,'bold'),bg='green',fg='black',width=10)
    lbl_pass.place(relx=.3,rely=.35)

    e_pass=Entry(frm,font=('calibri',20,'bold'),bd=5,show='**')
    e_pass.place(relx=.43,rely=.35)

    submit_button=Button(frm,text='SUBMIT',bg='light green',width=8,font=('calibri',18,'bold'),bd=5,command=submit_click)
    submit_button.place(relx=.37,rely=.5)

    reset_button=Button(frm,text='RESET',bg='light green',width=8,font=('calibri',18,'bold'),bd=5,command=reset_click)
    reset_button.place(relx=.5,rely=.5)

    fp_button=Button(frm,text='Forgot Password',bg='light green',width=14,font=('calibri',18,'bold'),bd=5,command=fp_click)
    fp_button.place(relx=.4,rely=.64)






def newuser_screen():
    def back():
        frm.destroy()
        main_screen()
        
    def createacn_db():
        name=e_name.get()
        email=e_mail.get()
        mob=e_mobile.get()
        adhar=e_adhar.get()

        if len(name)==0 or len(email)==0 or len(mob)==0 or len(adhar)==0:
            messagebox.showwarning("New User","Empty fields are not allowed")
            return

        match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning("New User","Invalid email")
            return
        
        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("New User","Invalid mob number.")
            return
        
        match=re.fullmatch(r"[0-9]{12}",adhar)
        if match==None:
            messagebox.showwarning("New User","Invalid adhar number.")
            return
        
        
        
        bal=0
        opendate=datetime.now()
        pwd=generator.generate_pass()
        query='''insert into accounts values(?,?,?,?,?,?,?,?)'''
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        curobj.execute(query,(None,name,pwd,mob,email,adhar,bal,opendate))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select max(acn) from accounts'''
        curobj.execute(query)
        tup=curobj.fetchone()
        conobj.close()
        Email_handler.send_credentials(email,name,tup[0],pwd)

        messagebox.showinfo('Account Creation','Your account is opened \nWe have mailed your credentials to given email')


    frm = Frame(root, highlightbackground='black', highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.15, relwidth=1, relheight=.8)

    back_button=Button(frm,text='BACK',bg='light green',font=('calibri',18,'bold'),bd=5,command=back)
    back_button.place(relx=0,rely=0)

    lbl_name=Label(frm,text='👨‍💼Name',font=('calibri',20,'bold'),bg='green',fg='black',width=7)
    lbl_name.place(relx=.1,rely=.2)

    e_name=Entry(frm,font=('calibri',20,'bold'),bd=5)
    e_name.place(relx=.2,rely=.2)
    e_name.focus()

    lbl_email=Label(frm,text='📧Email',font=('calibri',20,'bold'),bg='green',fg='black',width=7)
    lbl_email.place(relx=.1,rely=.3)

    e_mail=Entry(frm,font=('calibri',20,'bold'),bd=5)
    e_mail.place(relx=.2,rely=.3)

    lbl_mobile=Label(frm,text='📱Mobile',font=('calibri',20,'bold'),bg='green',fg='black',width=7)
    lbl_mobile.place(relx=.5,rely=.2)

    e_mobile=Entry(frm,font=('calibri',20,'bold'),bd=5)
    e_mobile.place(relx=.6,rely=.2)

    lbl_adhar=Label(frm,text='📄Adhar',font=('calibri',20,'bold'),bg='green',fg='black',width=7)
    lbl_adhar.place(relx=.5,rely=.3)

    e_adhar=Entry(frm,font=('calibri',20,'bold'),bd=5)
    e_adhar.place(relx=.6,rely=.3)

    submit_button=Button(frm,text='SUBMIT',bg='light green',width=8,font=('calibri',18,'bold'),bd=5,command=createacn_db)
    submit_button.place(relx=.37,rely=.5)

    reset_button=Button(frm,text='RESET',bg='light green',width=8,font=('calibri',18,'bold'),bd=5,command=back)
    reset_button.place(relx=.5,rely=.5)

    

def main_screen():
    def newuser_click():
        frm.destroy()
        newuser_screen()

    def existuser_click():
        frm.destroy()
        existuser_screen()

    frm = Frame(root, highlightbackground='black', highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.15, relwidth=1, relheight=.8)

    welcome = Label(
    frm,
    text='Welcome to the Banking Simulation Portal Experience Secure and Smart Banking',
        font=('times new roman', 25, 'bold',),
        bg='pink',
        fg='blue'
    )
    welcome.place(relx=0.5, rely=0.1, anchor='center')

    newuser_btn=Button(frm,
    text='New user\nCreate account',
    font=('calibri',20,'bold'),activebackground='yellow',fg='black',bg='light green',width=12,command=newuser_click
    )
    newuser_btn.place(relx=0.35, rely=0.37)

    existinguser_btn=Button(frm,
    text='Existing user\nLogin',
    font=('calibri',20,'bold'),activebackground='yellow',fg='black',bg='light green',width=12,command=existuser_click
    )
    existinguser_btn.place(relx=0.5, rely=0.37)



main_screen()
root.mainloop()

