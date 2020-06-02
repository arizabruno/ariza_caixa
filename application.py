from flask import Flask, render_template, request
import datetime
import sqlite3

##########################################################
# GLOBAL VARIABLES #######################################
##########################################################

# Creating a Data Base Object (Probably with the cs50 library)
# db = sqlite3.connect('ariza.db')
# cursor = db.cursor()

# Creating an variable to store the employe's name
# FUNCIONARIO_GLOBAL = ""
# Generating a variable with the date of the day (changes every day) ** TO DO : the date is not always right
data = datetime.date.today();

# Formating the date day-month-year
f_data=(data.strftime('%d/%m/%Y'))


# Formating the hour and minutes
horario_agora = datetime.datetime.now()
hora = horario_agora.hour
minutos = horario_agora.minute
horario = "" + str(hora) + ":" + str(minutos)


# Web app
app = Flask(__name__)


ACESSO_LIBERADO = False



###############################################################################################################################
                                                        #ENTRAR#
###############################################################################################################################



##########################################################
# DATA BASE FUNCTIONS ####################################
##########################################################



# Getting the data of all the 'funcionarios' registered
def funcionarios_sql():

    # Connecting with the DB
    db = sqlite3.connect('ariza.db')
    
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM funcionarios")
    funcionarios=cursor.fetchall()
    # Returning a dictionary as result
    return funcionarios
    
    
# Getting the data of all the 'administradores' registered
def administradores_sql():
    # Connecting with the DB
    db = sqlite3.connect('ariza.db')
    
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM administradores")
    administradores=cursor.fetchall()
    # Returning a dictionary as result
    return administradores 
   


##########################################################
# PAGINA INICIAL #########################################
##########################################################

@app.route("/", methods=['GET', 'POST'])
def index():
    # Ativando um elemento do CSS para o navbar
    active = "active"
    
    # Div Class
    dc = "container"
        
    # Control variables
    global ACESSO_LIBERADO
    ACESSO_LIBERADO = False
    liberar_msg = False
    
    # Getting a dictionary with all the 'funcionarios' and one with all the 'administradores'
    funcionarios = funcionarios_sql()
    administradores = administradores_sql()

     # If 'POST' method
    if request.method == 'POST':
    
        # Checking if the user is a 'funcionario' or a 'administrador'
        if request.form['posicao'] == 'func': 
        
            # Cheking if the name and password that the user inputed is valid
            for funcionario_a in funcionarios:
                if funcionario_a['funcionario'] == request.form['usuario'] and funcionario_a['senha'] == request.form['senha']:
                    
                    # If the input is valid creating a GLOBAL variable to the 'funcionario' name
                    global FUNCIONARIO_GLOBAL
                    FUNCIONARIO_GLOBAL = funcionario_a['funcionario']
                    
                    # Giving access to the user
                    ACESSO_LIBERADO = True
                    
                    # Bootstrap
                    dc = "container-fluid"
                    
                    return render_template('funcs/pagina_inicial_func.html', dc=dc, data=f_data, nome_func=FUNCIONARIO_GLOBAL, pet_total="--", clinica_total="--", laboratorio_total="--", banhoetosa_total="--", transporte_total="--", valor_total="--")
                else:
                    liberar_msg = True
        elif request.form['posicao'] == 'admin':
            # Cheking if the name and password that the user inputed is valid
            for administrador_a in administradores:
                if administrador_a['administrador'] == request.form['usuario'] and administrador_a['senha'] == request.form['senha']:
                    
                    # If the input is valid creating a GLOBAL variable to the 'administrador' name
                    global ADMINISTRADOR_GLOBAL
                    ADMINISTRADOR_GLOBAL = administrador_a['administrador']
                    
                    # Giving access to the user
                    ACESSO_LIBERADO = True
                   
                    # Bootstrap
                    dc = 'container-fluid'
                    
                    return render_template('adm/pagina_inicial_adm.html', dc=dc, data=f_data, nome_adm=ADMINISTRADOR_GLOBAL, pet_total="--", clinica_total="--", laboratorio_total="--", banhoetosa_total="--", transporte_total="--", valor_total="--")
                else:
                    liberar_msg = True
     
            
        # Returning de page to be displayed
        return render_template('index.html', active=active, dc=dc, liberar_msg=liberar_msg)
    
 

    # Returning the page to be displayed
    return render_template('index.html', active=active, dc=dc, funcionarios = administradores)
    

    



###############################################################################################################################
                                                        #ADMINISTRADORES#
###############################################################################################################################

##########################################################
# DATA BASE FUNCTIONS ####################################
##########################################################



# Filter query, method used to visualize the 'entradas' data base filtering using parameters
def adm_vis_sql(id_input, metodo, cond, valor, funcionario, data, cliente):

    
    # Building the query
    
    and_id_script = " AND "
    and_metodo_script = " AND "
    and_cond_script = " AND "
    and_valor_script = " AND "
    and_func_script = " AND "
    and_data_script = " AND "
    and_cliente_script = " AND "


    id_script = "id = " + str(id_input)
    metodo_script = " metodo LIKE " + "'" + metodo + "'"
    cond_script = "cond LIKE " + "'" + cond + "'"
    valor_script = "valor = " + str(valor)
    func_script = "funcionario LIKE " + "'" + funcionario + "'"
    data_script = "data LIKE " + "'" + data + "'"
    client_script = "cliente LIKE " + "'" + cliente + "'"

    where_script = " WHERE "

    if id_input == "" and cond == "" and metodo == "" and valor == "" and funcionario == "" and data == "" and cliente == "":
        where_script =""

    if id_input == "":
        id_script = ""
        and_metodo_script = ""

    if metodo == "":
        and_metodo_script = ""
        metodo_script = ""
        and_cond_script = ""

    if cond == "":
        and_cond_script = ""
        cond_script = ""
        and_valor_script = ""

    if valor == "":
        and_valor_script = ""
        valor_script = ""
        and_func_script = ""

    if funcionario == "":
        func_script = ""
        and_func_script = ""
        and_data_script = ""
	
    if data == "":
        data_script = ""
        and_data_script = ""
        and_cliente_script = ""

    if cliente == "":
        and_cliente_script = ""
        client_script = ""


    # Final query:
    mensagem = "SELECT * FROM entradas" + where_script + id_script + and_metodo_script + metodo_script + and_cond_script + cond_script + and_valor_script + valor_script + and_func_script + func_script + and_data_script + data_script + and_cliente_script + client_script

    
    
    # Connecting with the DB
    db = sqlite3.connect('ariza.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(mensagem)
    rows=cursor.fetchall()
    return rows
    

# Deleting an user 
def delete_user(tabela, id):

    condicao = "(id = ?)"
    mensagem = "DELETE FROM" + " '" + tabela + "' " + "WHERE " + condicao
    db = sqlite3.connect('ariza.db')
    cursor = db.cursor()
    db.execute(mensagem, (id, ))
    db.commit()
    
 
# Add an user
def add_user(tabela, nome, senha):
    # INSERT INTO administradores (administrador, senha, data) VALUES ('jose', '123', '111');
    
    if tabela == 'administradores':
        mensagem = "INSERT INTO " + tabela + " (administrador, senha, data) VALUES " + "(" + "'" + nome + "'" + ","+ "'" + senha + "'" +"," + "'" + f_data + "'" + ")" 
    else:
        mensagem = "INSERT INTO " + tabela + " (funcionario, senha, data) VALUES " + "(" + "'" + nome + "'" + ","+ "'" + senha + "'" +"," + "'" + f_data + "'" + ")" 

    db = sqlite3.connect('ariza.db')
    cursor = db.cursor()
    db.execute(mensagem)
    db.commit()
    
# Getting the Totals from the day
def total_function_adm():
    db = sqlite3.connect('ariza.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("SELECT SUM(pet), SUM(clinica), SUM(laboratorio), SUM(banhoetosa), SUM(transporte), SUM(valor) FROM entradas WHERE data LIKE (?)", (f_data, ))
    total_array = cursor.fetchall()    

    return total_array




##########################################################
# PAGINA DOS ADIMINISTRADORES ############################
##########################################################

@app.route("/adm_inicio")
def adm_page():
    
    # Checking if the user has logged 
    if ACESSO_LIBERADO == False:
        return render_template('index.html', dc='container')

    # Ativando um elemento do CSS para o navbar
    active = "active"
    
    # Div Class
    dc = "container-fluid"
    
    total = total_function_adm()
        
    # Setting the totals of each sector to its due variable
    pet_total = total[0][0]
    clinica_total = total[0][1]
    laboratorio_total = total[0][2]
    banhoetosa_total = total[0][3]
    transporte_total = total[0][4]
    valor_total = total[0][5]
    
    # Checking if there is at least one 'entrada' in the day - changing the 'None'
    if str(pet_total) == 'None':
        pet_total = 0.00
        clinica_total = 0.00
        laboratorio_total = 0.00
        banhoetosa_total = 0.00
        transporte_total = 0.00
        valor_total = 0.00
    
   
    # Returning de page to be displayed
    return render_template('adm/pagina_inicial_adm.html', dc=dc, data=f_data, nome_adm=ADMINISTRADOR_GLOBAL, pet_total=pet_total, clinica_total=clinica_total, laboratorio_total=laboratorio_total, banhoetosa_total=banhoetosa_total, transporte_total=transporte_total, valor_total=valor_total)



##########################################################
# PAGINA DA VISUALIZACAO #################################
##########################################################

@app.route("/adm_vis", methods=['GET', 'POST'])
def adm_visualizar():

    # Checking if the user has logged 
    if ACESSO_LIBERADO == False:
        return render_template('index.html', dc='container')

    # Ativando um elemento do CSS para o navbar
    active = "active"
    
    # Div Class
    dc = "container-fluid"

    # If 'POST' method
    if request.method == 'POST':
    
        # Getting the search paramenters
        if request.form['id'] == "":
            id_input = ""
        else:
            id_input = int(request.form['id'])
        metodo_input = request.form['metodo']
        cond_input = request.form['cond']
        if request.form['valor'] == "":
            valor_input = ""
        else:
            valor_input = float(request.form['valor'])
        func_input = request.form['funcionario']
        data_input = request.form['data']
        cliente_input = request.form['cliente']

        rows_adm_vis = adm_vis_sql(id_input, metodo_input, cond_input, valor_input, func_input, data_input, cliente_input)

    
        return render_template('adm/adm_visualizar.html', entradas=rows_adm_vis, data=f_data, dc=dc)


    # Returning de page to be displayed
    return render_template('adm/adm_visualizar.html', dc=dc)
    
    
    
##########################################################
# GEREAMENTO DE USUARIOS #################################
##########################################################   

@app.route("/deletar_usuarios", methods=['GET', 'POST'])
def deletar_usuarios():

    # Checking if the user has logged 
    if ACESSO_LIBERADO == False:
        return render_template('index.html', dc='container')

    # Ativando um elemento do CSS para o navbar
    active = "active"
    
    # Div Class
    dc = "container"
    
    mensagem = " "

    # If 'POST' method
    if request.method == 'POST':
    
        if request.form['posicao'] == 'admin':
            administradores_a = administradores_sql()
            id_valido = False
            # Making sure that the employe actually typed an ID
            if request.form['id'] == "":
                mensagem = "negado"
            else:
                # Getting the user input
                id_to_delete = float(request.form['id'])

                # Chacking if the input actually exists
                for j in administradores_a:
                    if j['id'] == id_to_delete:
                        id_valido = True
                
            # If the input exists, then delete
            if id_valido:
                mensagem = "sucesso"
                #db.execute("DELETE FROM entradas WHERE (rowid = :id)", id=id_to_delete)
                delete_user('administradores', id_to_delete)
            else:
                mensagem = "negado"
        else:
            funcionarios_a = funcionarios_sql()
            id_valido = False
            # Making sure that the employe actually typed an ID
            if request.form['id'] == "":
                mensagem = "negado"
            else:
                # Getting the user input
                id_to_delete = float(request.form['id'])

                # Chacking if the input actually exists
                for j in funcionarios_a:
                    if j['id'] == id_to_delete:
                        id_valido = True
            
            # If the input exists, then delete
            if id_valido:
                mensagem = "sucesso"
                #db.execute("DELETE FROM entradas WHERE (rowid = :id)", id=id_to_delete)
                delete_user('funcionarios', id_to_delete)
            else:
                mensagem = "negado"

           
        # Returning de page to be displayed
        return render_template('adm/deletar_usuarios.html', mensagem=mensagem, active_del=active, dc=dc)
        
        
      

    # Returning de page to be displayed
    return render_template('adm/deletar_usuarios.html', active_del=active, dc=dc)
    
@app.route("/adicionar_usuarios", methods=['GET', 'POST'])
def adicionar_usuarios():
    # Checking if the user has logged 
    if ACESSO_LIBERADO == False:
        return render_template('index.html', dc='container')

    # Ativando um elemento do CSS para o navbar
    active = "active"
    
    # Div Class
    dc = "container"
    
    mensagem = " "
    
    # If 'POST' method
    if request.method == 'POST':
        if request.form['nome_ad'] != "" and request.form['senha_ad'] != "" and request.form['posicao_ad'] != "":
            nome_ad = request.form['nome_ad']
            senha_ad = request.form['senha_ad']
            posicao_ad = request.form['posicao_ad'] 
            add_user(posicao_ad, nome_ad, senha_ad)
            mensagem = "sucesso"
        else:
            mensagem = "negado"
        
        return render_template('adm/adicionar_usuarios.html', mensagem=mensagem, active_del=active, dc=dc)
        
    return render_template('adm/adicionar_usuarios.html', mensagem=mensagem, active_del=active, dc=dc)
    
    
##########################################################
# USUARIOS ###############################################
##########################################################
    
# Displaying all the 'funcionarios' and 'administradores'    
@app.route('/usuarios')
def usuarios():

    # Checking if the user has logged 
    if ACESSO_LIBERADO == False:
        return render_template('index.html', dc='container')

    # Div class
    dc = 'container'
    
    funcionarios_a = funcionarios_sql()
    administradores_a = administradores_sql()
    return render_template('adm/usuarios.html', funcionarios=funcionarios_a, administradores=administradores_a, dc=dc)


###############################################################################################################################
                                                         #FUNCIONARIOS#
###############################################################################################################################


##########################################################
# DATA BASE FUNCTIONS ####################################
##########################################################

# Getting the data from the TABLE: entradas and returning everithing but the name of the employe and the date
def vis_data():
    db = sqlite3.connect('ariza.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM entradas WHERE (funcionario = ?) AND data LIKE (?)", (FUNCIONARIO_GLOBAL, f_data))
    rows=cursor.fetchall()
    return rows

# Deletting a row according to the ID
def delete_by_id(id):
    db = sqlite3.connect('ariza.db')
    cursor = db.cursor()
    db.execute("DELETE FROM entradas WHERE (rowid = ?) AND funcionario LIKE (?)", (id, FUNCIONARIO_GLOBAL))
    db.commit()


# Inserting a new row in the data base
def nova_entrada(metodo, valor, pet, clinica, laboratorio, transporte, banhoetosa, cond, cliente, funcionario, format_data, horario_f):
    db = sqlite3.connect('ariza.db')
    cursor = db.cursor()
    db.execute("INSERT INTO entradas (id,metodo,valor,pet,clinica,laboratorio,transporte,banhoetosa,cond,cliente,funcionario,data, horario) VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?)", (metodo, valor, pet, clinica, laboratorio, transporte, banhoetosa, cond, cliente, funcionario, format_data, horario_f))          
    db.commit()
    
# Getting the Totals from the day
def total_function():
    db = sqlite3.connect('ariza.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("SELECT SUM(pet), SUM(clinica), SUM(laboratorio), SUM(banhoetosa), SUM(transporte), SUM(valor) FROM entradas WHERE data LIKE (?) AND funcionario LIKE (?)", (f_data, FUNCIONARIO_GLOBAL))
    total_array = cursor.fetchall()    

    return total_array

##########################################################
# PAGINA DOS FUNCIONARIOS ################################
##########################################################

@app.route("/func_page")
def func_page():

    # Checking if the user has logged 
    if ACESSO_LIBERADO == False:
        return render_template('index.html', dc='container')

    # Ativando um elemento do CSS para o navbar
    active = "active"
    
    # Div Class
    dc = "container-fluid"
    
    total = total_function()
        
    # Setting the totals of each sector to its due variable
    pet_total = total[0][0]
    clinica_total = total[0][1]
    laboratorio_total = total[0][2]
    banhoetosa_total = total[0][3]
    transporte_total = total[0][4]
    valor_total = total[0][5]
    
    # Checking if there is at least one 'entrada' in the day - changing the 'None'
    if str(pet_total) == 'None':
        pet_total = 0.00
        clinica_total = 0.00
        laboratorio_total = 0.00
        banhoetosa_total = 0.00
        transporte_total = 0.00
        valor_total = 0.00
    
 
   
    # Returning de page to be displayed
    return render_template('funcs/pagina_inicial_func.html', dc=dc, data=f_data, nome_func=FUNCIONARIO_GLOBAL, pet_total=pet_total, clinica_total=clinica_total, laboratorio_total=laboratorio_total, banhoetosa_total=banhoetosa_total, transporte_total=transporte_total, valor_total=valor_total)


##########################################################
# PAGINA DA VISUALIZACAO #################################
##########################################################

@app.route("/vis")
def visualizar():

    # Checking if the user has logged 
    if ACESSO_LIBERADO == False:
        return render_template('index.html', dc='container')

    # Ativando um elemento do CSS para o navbar
    active = "active"

    # Calling vis_data() to return the data
    rows_vis = vis_data()
    
    # Div Class
    dc = "container-fluid" 

   
    # Returning de page to be displayed
    return render_template('funcs/visualizar.html', entradas=rows_vis, data=f_data, active_vis=active, dc=dc)


##########################################################
# PAGINA DELETE ##########################################
##########################################################

@app.route("/del", methods=['GET', 'POST'])
def deletar():
    
    # Checking if the user has logged 
    if ACESSO_LIBERADO == False:
        return render_template('index.html', dc='container')
    
    # Ativando um elemento do CSS para o navbar
    active = "active"
    
    # Div Class
    dc = "container"
    
    mensagem = " "

    # If 'POST' method
    if request.method == 'POST':

        # Storing the data a variable
        rows_del = vis_data()

        id_valido = False

        # Making sure that the employe actually typed an ID
        if request.form['id'] == "":
            mensagem = "negado"
        else:
            # Getting the user input
            id_to_delete = float(request.form['id'])

            # Chacking if the input actually exists
            for j in rows_del:
                if j['id'] == id_to_delete:
                    id_valido = True

        # If the input exists, then delete
        if id_valido:
            mensagem = "sucesso"
            #db.execute("DELETE FROM entradas WHERE (rowid = :id)", id=id_to_delete)
            delete_by_id(id_to_delete)
        else:
            mensagem = "negado"
        
            
            

        # Returning de page to be displayed
        return render_template('funcs/deletar.html', mensagem=mensagem, active_del=active, dc=dc)
        
        
      

    # Returning de page to be displayed
    return render_template('funcs/deletar.html', active_del=active, dc=dc)


##########################################################
# PAGINA DA NOVA ENTRADA #################################
##########################################################

@app.route("/send", methods=['GET', 'POST'])
def send():

    # Checking if the user has logged 
    if ACESSO_LIBERADO == False:
        return render_template('index.html', dc='container')

    # Ativando um elemento do CSS para o navbar
    active = "active"

    # If 'POST' method
    if request.method == 'POST':

        # Making sure all the input is valid, and then storing them in variables

        metodo = request.form['metodo']
        cond= request.form['cond']
        cliente = request.form['cliente']

        if request.form['pet'] == "":
            pet = 0
        else:
            pet = float(request.form['pet'])

        if request.form['clinica'] == "":
            clinica = 0
        else:
            clinica = float(request.form['clinica'])

        if request.form['laboratorio'] == "":
            laboratorio = 0
        else:
            laboratorio = float(request.form['laboratorio'])

        if request.form['transporte'] == "":
            transporte = 0
        else:
            transporte = float(request.form['transporte'])

        if request.form['banhoetosa'] == "":
            banhoetosa = 0
        else:
            banhoetosa = float(request.form['banhoetosa'])

        # Calculating the total
        valor = pet + clinica + laboratorio + transporte + banhoetosa

        # Calling nova_entrada -> generating a new row
        nova_entrada(metodo, valor, pet, clinica, laboratorio, transporte, banhoetosa, cond, cliente, FUNCIONARIO_GLOBAL, f_data, horario)

        # Calling vis_data() to return the data
        rows = vis_data()
        
        

        # Returning de page to be displayed
        return render_template('funcs/resultado.html', metodo=metodo, valor=valor, pet=pet, clinica=clinica, laboratorio=laboratorio, transporte=transporte, cond=cond, cliente=cliente, entradas=rows, funcionario=FUNCIONARIO_GLOBAL, data=data, active_ne=active)

    # Div Class
    dc = "container"    
    
    # Returning de page to be displayed
    return render_template('funcs/formulario.html', active_ne=active, dc=dc)
    
    
    
   
    




##########################################################
# INICIANDO O APP ########################################
##########################################################

if __name__ == "__main__":
  app.run(debug=True)



