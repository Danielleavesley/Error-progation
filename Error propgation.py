import tkinter
from tkinter import ANCHOR, SINGLE, Button, Widget, filedialog,ttk
from tkinter import *
import numpy as np
import pandas as pd
from sympy import symbols, diff
tkinter.Tk().withdraw() 
def File_slc(): #handles dioglog for browsing a file
    folder_path = filedialog.askopenfile(mode="r")
    return folder_path



def Equation_handle(): # handels taking an equation as text imput and finding the symblos within it
    equation=tkinter.simpledialog.askstring("equation", "What equation would you like to progate")
    global orignal_equation
    orignal_equation=equation
    chars=list(equation)
    chars.append("_")
    Symbols=[]
    temp=""
    for x in chars:
        if 65<=ord(x)<=90 or 97<=ord(x)<=122:
            temp=temp+x
        elif len(temp)>0:
            Present=False
            for y in Symbols:
                if y==temp:
                    Present=True
            if Present==False:
                Symbols.append(temp)
            temp=""

    return equation,Symbols



def file_handling(path): #deals with opening and formating the file and data
    data=pd.read_csv(path,keep_default_na=False)
    data_array=data.values.tolist()# both this and the line below put padas dataformta into arryes
    headers=list(data)
    org_data=[]
    temp=[]
    for coloum_index in range(0,len(headers)): #buntch of logic to try and sort data
        if "Error" in (headers[coloum_index].split("/")[0]) or "error" in (headers[coloum_index].split("/")[0]):
            if ((coloum_index+1)==len(headers)):
                #temp.append(headers[coloum_index-1])
                for row_index in range(0,len(data_array)):
                    if data_array[row_index][coloum_index]=="":
                        temp.append([data_array[row_index][coloum_index-1],0])
                    else:
                        temp.append([data_array[row_index][coloum_index-1],data_array[row_index][coloum_index]])
                org_data.append(temp)
                temp=[]
            elif len(temp)==0:
                print("ohh nnonnnnn")
            else:
                for row_index in range(0,len(data_array)):
                    if data_array[row_index][coloum_index]=="":
                        temp.append([data_array[row_index][coloum_index-1],0])
                    else:
                        temp.append([data_array[row_index][coloum_index-1],data_array[row_index][coloum_index]])
                org_data.append(temp)
                temp=[]
        else:
            if ((coloum_index+1)==len(headers)):
                #temp.append(headers[coloum_index])
                for row_index in range(0,len(data_array)):
                    temp.append([data_array[row_index][coloum_index-1],0])
                org_data.append(temp)
                temp=[]
            elif len(temp)==0:
                temp.append(headers[coloum_index])
            else: #temp has a header already in
                for row_index in range(0,len(data_array)):
                    temp.append([data_array[row_index][coloum_index-1],1000])
                org_data.append(temp)
                temp=[]
                temp.append(headers[coloum_index])
    return(org_data,headers)
#    org_data should end up beening orginsted as so
#    [[colume header1,[data point1, error],[data point2, error]]......[data pointn,error]    ,       [colume header2],[data point1, error],[data point2, error]......[data pointn,error]]
#     any data wil take the coulme to the right to be it error vaules if labled as error
#     if no error is presented then it wil lassumed to be 0



def Constant_handling():
    Constant_number=tkinter.simpledialog.askstring("constant", "how many contants does your equation have")
    try:
        int(Constant_number)
    except:
        print("not a number")
        Constant_handling()
        return
    else:
        Values={}
        for x in range(0,int(Constant_number)):
            Constant_Vaule=Constant_diolago(x)
            Values.update({x+1 :  Constant_Vaule})
        return(Values)
    

const_error=[]         

def Constant_diolago(x):
    Constant_Vaule=tkinter.simpledialog.askstring(f"constant {x+1}", f" what is Constant{x+1} vaule, to add error use +- between the value and error")
    constant_split=Constant_Vaule.split("+-")
    try:
        float(constant_split[0])
    except:
        print("not number")
        Constant_diolago(x)
        return
    else:
        const_error.append(constant_split)#should be [constant vaule,constant error]
        return float(constant_split[0])
    
     
def Selection(org_data,headers,Cont_dir,Symbols):
    button_cont()
    print(const_complete)



def button_cont():
    global x
    global berry
    global root
    global const_complete
    global Equation
    try:
        root.withdraw()
    except:
        print("fine")
    try:
        pick=berry.get(ANCHOR)
        const_complete.append(pick) 

        Symbols.remove(pick)
    except:
        print("fine")
    while x<len(Cont_dir):
        root = tkinter.Tk()
        root.title("Symblos to what they reersents")
        #window size
        root.geometry("800x500")


        #widgets
        label=ttk.Label(master=root, text=f"This Constant has a value of {Cont_dir[x+1]} \nwhat symbol repersents it").pack()
        box=tkinter.Listbox(master=root,selectmode=SINGLE , height=len(Symbols),width=50)
        for y in range(0,len(Symbols)): 
            box.insert(y+1, Symbols[y])
            box.pack()
        berry=box
        x=x+1
        if len(Cont_dir) == (len(const_complete)):
            ttk.Button(master=root,text="comfirm",command= root.destory ).pack()
        else:
            ttk.Button(master=root,text="comfirm",command= button_cont ).pack()
        root.mainloop()
    if len(Cont_dir) == (len(const_complete)):
        if len(Cont_dir)!=0:
            inserting_constants(const_complete)
        elif len(Cont_dir)==0:
            global new_Equation
            new_Equation=Equation
        berry=0
        button_Headers()

    return

#const_complete i belive is formated as in the order constant was selectedand just the symblo

def inserting_constants(const_complete):
    global Equation,Cont_dir,new_Equation ,Cont_dir_named                             #Cont_dir: it formates like {1:vaule , 2:vaule}  attaully just list constats saying it was the first or second contant to be asked
    Cont_dir_named=Cont_dir
    for n in range(1,len(Cont_dir)+1):
        Cont_dir_named[f"{const_complete[n-1]}"]=Cont_dir_named.get(n)
        Cont_dir_named.pop(n)                               ##Cont_dir_named: it is now formatted using the responding syblos rather than the order they was asked
    Equation_elements=list(Equation)
    for z in Cont_dir_named:
        temp=[]
        new_Equation=[]
        for y in range(0,len(Equation_elements)):
            temp.append(Equation_elements[y])
            new_Equation.append(Equation_elements[y])
            if len(temp)==len(z):
                temp2=""
                for n in temp:
                    temp2=temp2+n
                if temp2==z:
                    for m in range(0,len(z)):
                        new_Equation.pop(len(new_Equation)-1-m)
                    new_Equation.insert(len(new_Equation)-m,(f"({Cont_dir_named[f"{z}"]})"))
                temp.pop(0)
        Equation_elements=new_Equation
    temp=""
    for n in new_Equation:
        temp=temp+n
    new_Equation=temp
    global x
    x=0

    return



def button_Headers():
    global x
    global berry
    global windows
    global headers_complete
    global Symbols
    global no_error_headers
    try:
        windows.withdraw()
    except:
        print("fine")
    try:
        pick=berry.get(ANCHOR)
        headers_complete.append([pick,Symbols[x-1]]) 
        Symbols.remove(pick)
    except:
        print("fine")
    while x<len(Symbols):
        windows = tkinter.Tk()
        windows.title("Symblos to what they reersents")
        #window size
        windows.geometry("800x500")


        #widgets
        label=ttk.Label(master=windows, text=f"This symbol {f"{Symbols[x]}"} \nwhat symbol repersents it").pack()
        box2=tkinter.Listbox(master=windows,selectmode=SINGLE , height=len(no_error_headers),width=50)
        for y in range(0,len(no_error_headers)): 
            box2.insert(tkinter.END, no_error_headers[y])
        box2.pack()
        berry=box2
        x=x+1
        ttk.Button(master=windows,text="comfirm",command= button_Headers ).pack()
        windows.mainloop()
    windows.destroy()     #headers_complete is formated [[header,symbol],[header2,symblol2]]
    error_prop()
    return



def error_prop():
    global new_Equation,org_data,headers_complete,Equation #org data is all data where used_data is required data
    partial_diff=[]
    used_data=[]   # used_data formated [[[headers,symbol],[data for header1],[error for header1]],[[data for header2],[error for header2]]....]
    for x in headers_complete:
        partial_diff.append([(f"({str(diff(new_Equation,x[1]))})*")+(f"sigma_{x[1]}"),x[1]]) #partial_diff is formated like so [[partial diffrental,the sybol it was diffrent against] , []]
        print([(f"({str(diff(new_Equation,x[1]))})*")+(f"sigma_{x[1]}"),x[1]])
    for header in headers_complete:
        temp_data=[]
        temp_error=[]
        for data in org_data:
            if data[0]==header[0]:
                for data_index in range(1,len(data)):
                    if data[data_index][0]=="":
                        temp_data.append(0)
                    else:
                        temp_data.append(float(data[data_index][0]))
                    if data[data_index][1]=="":
                        temp_error.append(0)
                    else:
                        temp_error.append(float(data[data_index][1]))
        used_data.append([header,np.array(temp_data),np.array(temp_error)])
    for data in used_data:
        variable_name = f"{data[0][1]}"
        globals()[variable_name] = data[1]
        variable_name = f"sigma_{data[0][1]}"
        globals()[variable_name] = data[2]
    new_vaules=eval(new_Equation)
    temp_error=np.linspace(0,0,num=len(used_data[0][1]))

    ###dealing with error un contants
    #temp_partial=[]
    #temp_partial_replacment=[]
    #for y in range(0,len(const_complete)):
        #temp_partial=diff(orignal_equation,const_complete[y])
    #for y in temp_partial:
        #new_eq=y
       # for x in Cont_dir_named:
           # temp=""
           # temp_eq=""
           # for z in new_eq.split():
               # temp=temp+z
               # if len(temp)==len(x):
                   # if temp==x:
                      #  temp_eq=temp_eq+Cont_dir_named[f"{x}"]
                      #  temp=""
                   # else:
                      #  temp_eq=temp_eq+temp[0]

        



    for partial in partial_diff:
        print(sigma_w,sigma_l)
        print(temp_error,partial,str(partial[0]))
        temp_error=temp_error+(eval(str(partial[0])))**2
    print(np.sqrt(temp_error))
    new_error=np.sqrt(temp_error)
    new_file={}
    for data in org_data:
        new_file.update({(f"{data[0]}"):[],(f"{data[0]} error"):[]})
        new_file_data=[]
        new_file_error=[]
        for x in range(1,len(data)):
            new_file_data.append(data[x][0])
            new_file_error.append(data[x][1])
        new_file[f"{data[0]}"]=new_file_data
        new_file[f"{data[0]} error"]=new_file_error

    new_file.update({"new vaules":new_vaules})
    new_file.update({"new vaules error":new_error})
    df = pd.DataFrame(new_file)
    global path
    path_split=(path.name).split(r"/")
    file_name=((path_split[len(path_split)-1]).split(".")[0])
    path_split.pop(len(path_split)-1)
    new_path=""
    for i in path_split:
        new_path=new_path+(f"{i}/")
    df.to_csv(new_path+file_name+"_Propgated.csv", index=False)
    print("new file Created")



global berry, root, windows, const_complete, headers_complete
berry=0
root=0
windows=0
const_complete=[] 
headers_complete=[]
global x , no_error_headers
x=0
global no_error_headers
no_error_headers=[]
def main():
    global org_data, headers,Cont_dir,Symbols
    Inital_results=File_slc()
    global Equation  
    Equation,Symbols=Equation_handle()
    Cont_dir=Constant_handling()
    global path
    path=Inital_results
    org_data,headers=file_handling(Inital_results)
    for x in org_data:
        no_error_headers.append(x[0])
    Selection(org_data,headers,Cont_dir,Symbols)
main()