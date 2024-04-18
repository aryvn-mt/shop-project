import tkinter
import sqlite3

cnt=sqlite3.connect("shop.db")
session=False
#---------------- functions----------------
def submit():
    def SubNow():
        global session
        user = txt_user.get()
        pas = txt_pass.get()
        addr = txt_addr.get()
        sql = f'''SELECT * FROM users WHERE username="{user}" AND password="{pas}"'''
        result = cnt.execute(sql)
        rows = result.fetchall()
        if len(rows) > 0:
            lbl_msg3.configure(text="username already exist", fg="red")
        if user == "" or pas == "":
            lbl_msg3.configure(text="please fill the blanks!", fg="red")
        else:
            lbl_msg3.configure(text="you are submitted now!", fg="green")
            txt_user.delete(0, "end")
            txt_pass.delete(0, "end")
            txt_vpas.delete(0, "end")
            txt_addr.delete(0,"end")
            sql = f'''INSERT INTO users (username,password,address)
                        VALUES ("{user}","{pas}","{addr}")'''
            cnt.execute(sql)
            cnt.commit()





    win_submit = tkinter.Toplevel(win)
    win_submit.title("submit")
    win_submit.geometry("400x300")

    lbl_user = tkinter.Label(win_submit, text="Username: ")
    lbl_user.pack()
    txt_user = tkinter.Entry(win_submit)
    txt_user.pack()

    lbl_pass = tkinter.Label(win_submit, text="Password: ")
    lbl_pass.pack()
    txt_pass = tkinter.Entry(win_submit)
    txt_pass.pack()

    lbl_vpas = tkinter.Label(win_submit, text="Confirm Password: ")
    lbl_vpas.pack()
    txt_vpas = tkinter.Entry(win_submit)
    txt_vpas.pack()

    lbl_addr = tkinter.Label(win_submit, text="Address: ")
    lbl_addr.pack()
    txt_addr = tkinter.Entry(win_submit)
    txt_addr.pack()

    lbl_msg3 = tkinter.Label(win_submit, text="")
    lbl_msg3.pack()

    btn_subm = tkinter.Button(win_submit, text="Submit Now", command=SubNow)
    btn_subm.pack()
def login():
    global session
    user=txt_user.get()
    pas=txt_pass.get()
    sql=f'''SELECT * FROM users WHERE username="{user}" AND password="{pas}" '''
    result=cnt.execute(sql)
    rows=result.fetchall()
    if len(rows)<1:
        lbl_msg.configure(text="wrong username or password!",fg="red")
    else:
        print(rows)
        session=rows[0][0]
        lbl_msg.configure(text="welcome to your account!",fg="green")
        txt_user.delete(0,"end")
        txt_pass.delete(0,"end")
        btn_login.configure(state="disabled")
        btn_logout.configure(state="active")
        btn_sub.configure(state="disabled")
        btn_shop.configure(state="active")

def logout():
    global session
    session=False
    btn_login.configure(state="active")
    btn_logout.configure(state="disabled")
    lbl_msg.configure(text="you are logged out now!",fg="green")
    btn_shop.configure(state="disabled")

def shop():
    def updateList():
        sql = '''SELECT * FROM products'''
        result = cnt.execute(sql)
        rows = result.fetchall()
        for product in rows:
            info = f"product id:{product[0]}     name:{product[1]}     price:{product[2]}     quantity:{product[3]}"
            lst_product.insert("end", info)

    def pvalidate(pid,pqnt):
        if pid=="" or pqnt=="":
            return False,"please fill the blanks!"
        #--
        pid=int(pid)
        pqnt=int(pqnt)
        sql=f'''SELECT * FROM products  WHERE id={pid}'''
        result=cnt.execute(sql)
        rows=result.fetchall()
        if len(rows)<1:
            return False,"invalid product id!"
        #--
        sql=f'''SELECT * FROM products WHERE id={pid} and qnt>{pqnt}'''
        result = cnt.execute(sql)
        rows = result.fetchall()
        if len(rows) < 1:
            return False, "not enough products!"
        #--
        return True,""

    def buy():
        pid=txt_id.get()
        pqnt=txt_qnt.get()
        result,errorMSG=pvalidate(pid,pqnt)
        if not result:
            lbl_msg2.configure(text=errorMSG,fg="red")
            return
        pid=int(pid)
        pqnt=int(pqnt)
        sql=f'''INSERT INTO cart (uid,pid,qnt) VALUES ({session},{pid},{pqnt})'''
        cnt.execute(sql)
        cnt.commit()
        #--
        sql=f'''UPDATE products SET qnt=qnt-{pqnt} WHERE id={pid}'''
        cnt.execute(sql)
        cnt.commit()
        #--
        lst_product.delete(0,"end")
        updateList()
        #--
        txt_id.delete(0,"end")
        txt_qnt.delete(0,"end")
        lbl_msg2.configure(text="product has been added to your cart!",fg="green")

    def viewcart():

        win_view = tkinter.Toplevel(win_shop)
        win_view.title("view cart")
        win_view.geometry("400x400")

        lst_product = tkinter.Listbox(win_view, width=50, height=5, font="arial")
        lst_product.pack(pady=10)

        pid=txt_id.get()
        pqnt=txt_qnt.get()

        # pid = int(pid)
        # pqnt = int(pqnt)

        sql = f'''SELECT * FROM products  WHERE id={pid}'''
        result = cnt.execute(sql)
        rows = result.fetchall()
        for product in rows:
            info = f"product id:{pid}    name:{product[1]}     price:{product[2]}     quantity:{pqnt}"
            lst_product.insert("end", info)


    win_shop=tkinter.Toplevel(win)
    win_shop.title("shop panel")
    win_shop.geometry("500x500")

    lst_product=tkinter.Listbox(win_shop,width=70,height=10,font="arial")
    lst_product.pack(pady=10)

    updateList()

    lbl_id=tkinter.Label(win_shop,text="Product id: ")
    lbl_id.pack()
    txt_id=tkinter.Entry(win_shop)
    txt_id.pack()

    lbl_qnt = tkinter.Label(win_shop,text="Products number: ")
    lbl_qnt.pack()
    txt_qnt = tkinter.Entry(win_shop)
    txt_qnt.pack()

    lbl_msg2=tkinter.Label(win_shop,text="")
    lbl_msg2.pack()

    btn_buy=tkinter.Button(win_shop,text="BUY NOW!",command=buy)
    btn_buy.pack()

    btn_cart=tkinter.Button(win_shop,text="view cart",command=viewcart)
    btn_cart.pack()

    win_shop.mainloop()
#----------- create window ----------------
win=tkinter.Tk()
win.geometry("300x250")

lbl_user=tkinter.Label(win,text="Username: ")
lbl_user.pack()
txt_user=tkinter.Entry(win)
txt_user.pack()

lbl_pass=tkinter.Label(win,text="Password: ")
lbl_pass.pack()
txt_pass=tkinter.Entry(win)
txt_pass.pack()

lbl_msg=tkinter.Label(win,text="")
lbl_msg.pack()

btn_login=tkinter.Button(win,text="Login",command=login)
btn_login.pack()

btn_sub = tkinter.Button(win, text="submit", command=submit)
btn_sub.pack()

btn_logout=tkinter.Button(win,text="Logout",command=logout, state="disabled")
btn_logout.pack()

btn_shop=tkinter.Button(win,text="Shop",command=shop, state="disabled")
btn_shop.pack()

win.mainloop()