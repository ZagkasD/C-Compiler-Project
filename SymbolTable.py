
import sys
import string

#Alfavito  minimal++

alphabet =['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
			'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
			
numbers=['1','2','3','4','5','6','7','8','9']
#prakseis=['+','-','*','/']

#telestes_sigkrisis=['<','>','=','<=','>=','<>']

#telestis_anathesis=':='

#diaxwristes=[';',',',':']

#symbola_omadopoihsis=['(',')','[',']']

#diaxorismoi_sxoliwn=['/*','*/','//']

#aggiles=['[',']']

#parentheseis=['(',')']

#anoigma_kleisimo_block=['{','}']

file = open(sys.argv[1], 'r')

boolean_times=['true', 'false']

#Xaraktires pinaka metavasewn

white_char=0
letters=1
num0=2
num1to9=3
plus=4
minus=5
multiply=6
divide=7
equal=8
less_than=9
greater_than=10
EOF=11
oxi_apodekto_simvolo=12
koma=13
erwtimatiko=14
arist_parenthesi=15
deksia_parenthesi=16
arist_agkili=17
deksia_agkili=18
anoigma_block=19
kleisimo_block=20
allagi_grammis= 21
anwkatw_teleia=22


#Katastaseis

katastasi_start=0
katastasi_letter=1
katastasi_num0=2
katastasi_num1to9=3
katastasi_lessthan=4
katastasi_greaterthan=5
katastasi_anathesi=6
katastasi_anoigma_sxoliwn=7
katastasi_kleisimo_sxoliwn=8
typos_sxoliwn_1=9
typos_sxoliwn_2=10

#Tokens

id_tk=30
num_tk=31
plus_tk=32
minus_tk=33
multiply_tk=34
divide_tk=35
equal_tk=36
lessthan_tk=37
greaterthan_tk=38
EOF_tk=39
koma_tk=41
erwtimatiko_tk=42
arist_parenthesi_tk=43
deksia_parenthesi_tk=44
arist_agkili_tk=45
deksia_agkili_tk=46
anoigma_block_tk=47
kleisimo_block_tk=48
lessORequal_tk=49
greaterORequal_tk=50
anwkatw_teleia_tk=51
anathesi_tk=52
diaforo_tk=53  #addddddddddd


#DESMEUMENES LEKSEIS PROGRAMMATOS

desmeumenes_lexeis=['program' ,'declare' ,
					'if','then','else',
					'while','doublewhile','loop','exit',
					'forcase','incase','when','default',
					'not','and','or',
					'function','procedure','call','return','in','inout',
					'input','print']
					
					

program_tk=54
declare_tk=55
if_tk=56
then_tk=57
else_tk=58
while_tk=59
#doublewhile_tk=60
#loop_tk=61
#exit_tk=62
forcase_tk=63
#incnase_tk=64
when_tk=65
default_tk=66
procedure_tk=67
function_tk=68
call_tk=69
return_tk=70
in_tk=71
inout_tk=72
and_tk=73
or_tk=74
not_tk=75
input_tk=76
print_tk=77

#Errors

ERROR_MH_APODEKTO_SYMBOLO=-1
ERROR_0PSIFIO_NOUMERO=-2
ERROR_PSIFIO_GRAMMA=-3
ERROR_2_ANW_KATW_TELEIES=-4
ERROR_ARITHMOS_EKTOS_DIASTHMATOS=-5 
ERROR_LATHOS_ANOIGMA_PARENTHESEWN_AGKYLWN=-6
ERROR_MH_SWSTO_KLEISIMO_PARENTHESEWN_AGKYLWN=-7
ERROR_ANOIGMA_SXOLIW1_ME_EOF=-8



pinakas_metavasewn=[
	#katastasi_arxiki
	[katastasi_start,katastasi_letter,katastasi_num0,katastasi_num1to9,plus_tk,minus_tk,multiply_tk,
	 katastasi_anoigma_sxoliwn,equal_tk,katastasi_lessthan,katastasi_greaterthan,EOF_tk,ERROR_MH_APODEKTO_SYMBOLO,
	 koma_tk,erwtimatiko_tk,arist_parenthesi_tk,deksia_parenthesi_tk,arist_agkili_tk,deksia_agkili_tk,anoigma_block_tk,kleisimo_block_tk,
	 katastasi_start,katastasi_anathesi],
	# prepei na allaksw ta EROOR_MH_APODEKTO_.....
	#katastasi_letter
	[id_tk,katastasi_letter,katastasi_letter,katastasi_letter,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,ERROR_MH_APODEKTO_SYMBOLO,
	 id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk],
	#katastasi_num0
	[num_tk,ERROR_PSIFIO_GRAMMA,ERROR_0PSIFIO_NOUMERO,ERROR_0PSIFIO_NOUMERO,num_tk,num_tk,num_tk,
	 num_tk,num_tk,num_tk,num_tk,num_tk,ERROR_MH_APODEKTO_SYMBOLO,
	 num_tk,num_tk,num_tk,num_tk,num_tk,num_tk,num_tk,num_tk,
	 num_tk,num_tk],

	#katastasi_num1to9
	[num_tk,ERROR_PSIFIO_GRAMMA,katastasi_num1to9,katastasi_num1to9,num_tk,num_tk,num_tk,
	 num_tk,num_tk,num_tk,num_tk,num_tk,ERROR_MH_APODEKTO_SYMBOLO,
	 num_tk,num_tk,num_tk,num_tk,num_tk,num_tk,num_tk,num_tk,
	 num_tk,num_tk],

	#katastasi_lessthan
	[lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,
	 katastasi_anoigma_sxoliwn,lessORequal_tk,lessthan_tk,diaforo_tk,lessthan_tk,ERROR_MH_APODEKTO_SYMBOLO,
	 lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,
	 lessthan_tk,lessthan_tk],

	#katastasi_greaterthan
	[greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,
	 katastasi_anoigma_sxoliwn,greaterORequal_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,ERROR_MH_APODEKTO_SYMBOLO,
	 greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,
	 greaterthan_tk,greaterthan_tk],

	#katastasi_anathesi
	[anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,
	 anwkatw_teleia_tk,anathesi_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,ERROR_MH_APODEKTO_SYMBOLO,
	 anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,
	 anwkatw_teleia_tk,ERROR_2_ANW_KATW_TELEIES],

	#katastasi_anoigma_sxoliwn
	[divide_tk,divide_tk,divide_tk,divide_tk,divide_tk,divide_tk,typos_sxoliwn_1,
	 typos_sxoliwn_2,divide_tk,divide_tk,divide_tk,divide_tk,ERROR_MH_APODEKTO_SYMBOLO,
	 divide_tk,divide_tk,divide_tk,divide_tk,divide_tk,divide_tk,divide_tk,divide_tk,
	 divide_tk,divide_tk],

	#katastasi_kleisimo_sxoliwn
	[typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,katastasi_kleisimo_sxoliwn,
	 katastasi_start,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,ERROR_ANOIGMA_SXOLIW1_ME_EOF,typos_sxoliwn_1,
	 typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,
	 typos_sxoliwn_1,typos_sxoliwn_1],

	#typos_sxoliwn_1
	[typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,katastasi_kleisimo_sxoliwn,
	 typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,ERROR_ANOIGMA_SXOLIW1_ME_EOF,typos_sxoliwn_1,
	 typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,typos_sxoliwn_1,
	 typos_sxoliwn_1,typos_sxoliwn_1],


	#typos_sxoliwn_2
	[typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,
	 typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,katastasi_start,typos_sxoliwn_2,
	 typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,typos_sxoliwn_2,
	 katastasi_start,typos_sxoliwn_2]

	]

		

line=1


def lex():
	global line
	prod_wrd=''
	numOfdigits=0  #5psifios metaksi -32767 kai 32767
	over30= False
	current= katastasi_start
	
	linecounter= line
	resultlex=[]
	while(current>=0 and current<=11):
		char = file.read(1)

		if (char == ' ' or char == '\t'):
			char_tk = white_char
		elif (char in alphabet):
			char_tk = letters
		elif (char == '0'):
			char_tk = num0
		elif (char in numbers):
			char_tk = num1to9
		elif (char == '+'):
			char_tk = plus
		elif (char == '-'):
			char_tk = minus
		elif (char == '*'):
			char_tk = multiply
		elif (char == '/'):
			char_tk = divide
		elif(char == '='):
			char_tk = equal
		elif (char == '<'):
			char_tk = less_than
		elif (char == '>'):
			char_tk = greater_than
		elif (char == ':'):
			char_tk = anwkatw_teleia
		elif (char == ','):
			char_tk = koma
		elif (char == ';'):
			char_tk = erwtimatiko
		elif (char == '('):
			char_tk = arist_parenthesi
		elif (char == ')'):
			char_tk = deksia_parenthesi
		elif (char == '['):
			char_tk = arist_agkili
		elif (char == ']'):
			char_tk = deksia_agkili
		elif (char == '{'):
			char_tk = anoigma_block
		elif (char == '}'):
			char_tk = kleisimo_block
		elif (char == '\n'):
			linecounter=linecounter+1
			char_tk = allagi_grammis
		elif(char == '\r'):
			char_tk = allagi_grammis
		elif (char == ''):  # H EOF tha epistrepsei sto telos tou arxeiou   to  ''
			char_tk = EOF
		else:
			char_tk = oxi_apodekto_simvolo

		current=pinakas_metavasewn[current][char_tk]

		if(len(prod_wrd)<30):
			if(current!=katastasi_anoigma_sxoliwn and current!=typos_sxoliwn_1 and current!=typos_sxoliwn_2 and current!=katastasi_kleisimo_sxoliwn):
				if(current!=katastasi_start):
					prod_wrd+=char
			else:
				if(len(prod_wrd)==0):
					prod_wrd=''
			if (current == katastasi_num1to9):
				numOfdigits += 1

		else:
			print("H leksi exei panw apo 30 xarakthres, tha agnoithoun.")
			over30 = True


#Mexri edw exw brei tk!!!!!!!

	if(current==id_tk or
			   current==num_tk or
			   current==lessthan_tk or
			   current==greaterthan_tk or
			   current==divide_tk or current==anwkatw_teleia_tk ):
		if (char == '\n'):
			linecounter -= 1
		char=file.seek(file.tell()-1,0)  #epistrefei to teleutaio char pou diabase sto File (px avd+)

		prod_wrd = prod_wrd[:-1]	#kovei to +

	if(current==divide_tk):
		prod_wrd='/'

	#EINAI H EIDIKH PERIPTWSH POU EXOUME '{' kai meta EOF H KENO
	#print(prod_wrd)
	if(prod_wrd=='}' and current==-1):
		current= kleisimo_block_tk

	if(current==id_tk):
		if(prod_wrd in desmeumenes_lexeis):
			if(prod_wrd=='program'):
				current=program_tk
			elif(prod_wrd=='declare'):
				current=declare_tk
			elif (prod_wrd == 'if'):
				current = if_tk
			elif (prod_wrd=='then'):
				current = then_tk
			elif (prod_wrd == 'else'):
				current = else_tk
			elif (prod_wrd == 'while'):
				current = while_tk
			#elif (prod_wrd == 'doublewhile'):
				#current = doublewhile_tk
			#elif (prod_wrd == 'loop'):
				#current = loop_tk
			#elif (prod_wrd == 'exit'):
				#current = exit_tk
			elif (prod_wrd == 'forcase'):
				current = forcase_tk
			#elif (prod_wrd == 'incase'):
				#current = incnase_tk
			elif (prod_wrd == 'when'):
				current = when_tk
			elif (prod_wrd == 'default'):
				current = default_tk
			elif (prod_wrd == 'procedure'):
				current = procedure_tk
			elif (prod_wrd == 'function'):
				current = function_tk
			elif (prod_wrd == 'call'):
				current = call_tk
			elif (prod_wrd == 'return'):
				current = return_tk
			elif (prod_wrd == 'in'):
				current = in_tk
			elif (prod_wrd == 'inout'):
				current = inout_tk
			elif (prod_wrd == 'and'):
				current = and_tk
			elif (prod_wrd == 'or'):
				current = or_tk
			elif (prod_wrd == 'not'):
				current = not_tk
			elif (prod_wrd == 'input'):
				current = input_tk
			elif (prod_wrd == 'print'):
				current = print_tk


	#PERIORISMOS ARITHMOU PSIFIWN ALLA KAI TOU DIASTHMATOS [-32767,32767]
	if (current == num_tk):
		if (numOfdigits > 5):
			print("ERROR: O numOfdigits einai megalyteros apo 5 psifia")
			current = ERROR_ARITHMOS_EKTOS_DIASTHMATOS

	#Convert thn leksi se digit psifia
		if (prod_wrd.isdigit() < -32767 and prod_wrd.isdigit() > 32767):
			print("ERROR: O arithmos den einai sto diasthma [-32767,32767]")
			current = ERROR_ARITHMOS_EKTOS_DIASTHMATOS


	#ELEGXOS TWN ERRORS

	if(current==ERROR_MH_APODEKTO_SYMBOLO):
		print("ERROR: Exoume mh apodekto symbolo glwssas")
	elif(current==ERROR_0PSIFIO_NOUMERO):
		print("ERROR: Akolouthei noumero enw exei prohghthei 0")
	elif(current==ERROR_PSIFIO_GRAMMA):
		print("ERROR: Akolouthei gramma meta apo kapoio psifio")
	elif(current==ERROR_2_ANW_KATW_TELEIES):
		print("ERROR: Yparxoun 2 anw katw teleies synexomenes")
	elif(current==ERROR_ARITHMOS_EKTOS_DIASTHMATOS):
		print("ERROR: O arithmos den anikei sto diasthma [-32767,32767]")
	elif(current==ERROR_LATHOS_ANOIGMA_PARENTHESEWN_AGKYLWN):
		print("ERROR: Den exoun anoi3ei swsta parentheseis h agkyles")
	elif(current==ERROR_MH_SWSTO_KLEISIMO_PARENTHESEWN_AGKYLWN):
		print("ERROR: Den exoun kleisei swsta parentheseis h agkyles")
	elif(current==ERROR_ANOIGMA_SXOLIW1_ME_EOF):
		print("ERROR: Ta sxolia /* anoi3an swsta alla den ekleisan sto telos tou arxeiou")

	#STIN THESH 0 TOY PINAKA EXOUME TO TOKEN
	#STIN THESH 1 TOY PINAKA EXOUME THN LEXH POU SXHMATISE O LEKTIKOS ANALYTHS
	#STIN THESH 2 TOY PINAKA EXOUME TON ARITHMO GRAMMHS

	resultlex.append(current)
	resultlex.append(prod_wrd)
	resultlex.append(linecounter) #oxi aparaithto
	line=linecounter
	#print(resultlex)
	return resultlex


'''
########################################
	Synarthseis endiamesou kwdika
########################################
'''
global quadlist		#lista me Oles tis tetrades pou tha paraxthoun apo to programma.
quadlist = []
countQuad = 1		#O arithmos pou xarakthrizei thn tetrada. Brisketai mprosta apo thn 4ada.
def nextQuad():
	global countQuad
	
	return countQuad
def genQuad(first, second, third, fourth):
	global countQuad	#dhmiourgei epomenh tetrada, opou brosta exei ton arithmo ths (dhladh dhmiourgei 5ada ousiastika)
	global quadlist
	tlist = []
	
	tlist = [nextQuad()]			#Bazw prwta ton arithmo.
	tlist += [first] + [second] + [third] + [fourth]		#Epeita ta orismata
	
	countQuad +=1	#Ayksanw kata 1 ton arithmo ths epomenhs 4adas.
	quadlist += [tlist] 	#Put quad in global quadlist.

	return tlist

T_i = 1
tempList = []

def newTemp():
	'Dhmiourgei kai epistrefei mia nea proswrinh metablhth, ths morfhs T_1, T_2,.. .'
	global T_i
	global tempList
	
	list = ['T_']
	list.append(str(T_i))
	tempVariable="".join(list)
	T_i +=1
	tempList += [tempVariable]
	
	entt = Entity()								#Create an Entity
	entt.type = 'temp'
	entt.name = tempVariable				
	entt.tempVar.offset = compute_offset()	
	new_entity(ent)
	
	return tempVariable
def emptyList():
	'Dhmiourgei mia kenh lista etiketwn 4dwn.'
	pointerList = []
	
	return pointerList
def makeList(x):
	'Dhmiourgei mia lista etiketwn tetradwn pou periexei mono to x.'

	listThis = [x]
	
	return listThis
def merge(list1, list2):
	'Dhmiourgei mia lista etiketwn 4dwn apo th synenwsh listwn list1, list2.'
	list=[]
	list += list1 + list2

	return list

def backPatch(list, z):
	
	global quadlist
	
	for i in range(len(list)):
		for j in range(len(quadlist)):
			if(list[i]==quadlist[j][0] and quadlist[j][4]=='_'):
				quadlist[j][4] = z
				j=len(quadlist)	#to pass second loop faster and enter next i.
	return	


'''
########################################
'''

########################################
#SYNARTHSEIS PINAKA SYMVOLWN
########################################	

class Entity():

	def __init__(obj):
		obj.name = ''	#onoma Entity
		obj.type = ''
		obj.constant = ''
		obj.variable = obj.Variable()
		obj.subprogram = obj.SubProgram()
		obj.parameter = obj.Parameter()
		obj.tempVar = obj.TempVar()
		
	class Variable:
		def __init__(obj):
			obj.type = 'Int'
			obj.offset = 0				#Apostasi apo tin arxi tis stoivas

	class SubProgram:					
		def __init__(obj):
			obj.type = ''				
			obj.startQuad = 0			#Etiketa tis protis tetradas tou kwdika tis synartisi(h tetrada apo ton endiameso)
			obj.frameLength = 0			#Mikos egrafimatos drastiriopoihsis
			obj.argumentList = []		#h lista parametrwn (gia na apothikeuso ta TRIGONA)
			
	class Parameter:
		def __init__(obj):
			obj.mode = ''				
			obj.offset = 0				
	class TempVar:
		def __init__(obj):
			obj.type = 'Int'			
			obj.offset = 0

class Scope():
	def __init__(obj):
		obj.name = ''				#onoma Scope
		obj.entityList = []			#h lista apo entities
		obj.nestingLevel = 0		#Vathos foliasmatos
		obj.enclosingScope = None	#To Scope poy perikliei

class Argument():
	def __init__(obj):
		obj.name = ''		#onoma Argument
		obj.parMode = ''
		obj.type = 'Int'	

def new_entity(elem):  # neo Entity- Kitrino orthgonio
	global topScope
	
	topScope.entityList.append(elem)

def new_argument(elem): #neo Argument - Galazio trigwno
	global topScope
	
	topScope.entityList[-1].subprogram.argumentList.append(elem)

topScope = None

def new_scope(name):  # neo Scope - Kokkinos kuklos
	'create new scope'
	global topScope

	nextScope = Scope()
	nextScope.name = name
	nextScope.enclosingScope=topScope

	if(topScope == None):
		nextScope.nestingLevel = 0
	else:
		nextScope.nestingLevel = topScope.nestingLevel + 1

	topScope = nextScope

def delete_scope(): # diagrafi Scope - Kokkinos Kuklos
	global topScope
	
	freeScope = topScope
	topScope = topScope.enclosingScope

	del freeScope

def compute_offset():
	'Computes how many bytes '
	global topScope
	
	counter=0
	if(topScope.entityList != []):
		for ent in (topScope.entityList):
			if(ent.type == 'variable' or ent.type == 'temp' or ent.type=='param'):
				counter +=1
	offset = 12+(counter*4)
	
	return offset

def compute_startQuad():
	global topScope
	
	topScope.enclosingScope.entityList[-1].subprogram.startQuad = nextQuad()

def compute_framelength():
	global topScope
	
	topScope.enclosingScope.entityList[-1].subprogram.frameLength = compute_offset()
	
def add_parameters():
	global topScope
	
	for arg in topScope.enclosingScope.entityList[-1].subprogram.argumentList:
		ent = Entity()
		ent.name = arg.name
		ent.type = 'param'
		ent.parameter.mode = arg.parMode
		ent.parameter.offset = compute_offset()
		new_entity(ent)

def print_Symbol_table():
	global topscope
	
	print('Enarksi Pinaka Symvolwn.')
	
	ts = topScope
	
	while ts != None:
		print("SCOPE: "+"name:"+ts.name+" nestingLevel:"+str(ts.nestingLevel))
		
		print("\tENTITIES:")
		
		for ent in ts.entityList:
			if(ent.type == 'variable'):
				print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t variable-type:"+ent.variable.type+"\t offset:"+str(ent.variable.offset))
			elif(ent.type == 'temp'):
				print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t temp-type:"+ent.tempVar.type+"\t offset:"+str(ent.tempVar.offset))
			elif(ent.type == 'Subprogram'):
				if(ent.subprogram.type == 'Function'):
					print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t function-type:"+ent.subprogram.type+"\t startQuad:"+str(ent.subprogram.startQuad)+"\t frameLength:"+str(ent.subprogram.frameLength))
					print("\t\tARGUMENTS:")
					for arg in ent.subprogram.argumentList:
						print("\t\tARGUMENT: "+" name:"+arg.name+"\t type:"+arg.type+"\t parMode:"+arg.parMode)
				elif(ent.subprogram.type == 'Procedure'):
					print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t procedure-type:"+ent.subprogram.type+"\t startQuad:"+str(ent.subprogram.startQuad)+"\t frameLength:"+str(ent.subprogram.frameLength))
					print("\t\tARGUMENTS:")
					for arg in ent.subprogram.argumentList:
						print("\t\tARGUMENT: "+" name:"+arg.name+"\t type:"+arg.type+"\t parMode:"+arg.parMode)
			elif(ent.type == 'param'):
				print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t mode:"+ent.parameter.mode+"\t offset:"+str(ent.parameter.offset))

		ts = ts.enclosingScope

	print('Telos Pinaka Simvolwn.')

'''
###########################################
#SYNTAKTIKOS ANALYTHS
#ENDIAMESOS KWDIKAS
###########################################
'''
	
def syntax_an(cFILE):

	global tk
	tk = lex()
	
	global temp
	global flag
	flag = 0
	
	def program():
 
		global tk
		
		if(tk[0] == program_tk):
			tk = lex()

			ProgName=tk[1]
			
			if(tk[0] == id_tk):
				tk = lex()
				
				if(tk[0] == anoigma_block_tk):
					tk = lex()
					  
					block(ProgName,1)     #to 1 xreiazetai gia Halt
					if(tk[0] == kleisimo_block_tk):
						tk = lex()

						return
					else:
						print("ERROR: Den yparxei aggistro gia to kleisimo tou program", line)
						
						exit(-1)
				else:
					print("ERROR: Den yparxei aggistro gia to anoigma tou 'program' ",line)
					exit(-1)
			else:
				print("ERROR: Den yparxei onoma arxeiou/programmatos",line)
				exit(-1)
		else:
			 print("ERROR: H leksi 'program' den yparxei stin arxi tou programmatos",line)
			 exit(-1)

	def block(blockName , Program_flag):
		global tk
		
		declarations()
		
		subprograms()
		genQuad('begin_block',blockName,'_','_')

		statements()
		if(Program_flag==1):
			genQuad('halt','_','_','_')
		genQuad('end_block',blockName,'_','_')
		
		return
		
	def declarations():
		global tk 
		
		while(tk[0] == declare_tk):
			tk = lex()
			line = tk[2]
			
			varlist()
			
			if(tk[0] == erwtimatiko_tk):
				tk = lex()
				line = tk[2]
				
			else:
				print("ERROR: Den yparxei erwtimatiko sto telos tou varlist", line)
				exit(-1)
		return
				
	def varlist():
		global tk
		
		if(tk[0] == id_tk):
			entt1 = Entity()
			entt1.type = 'Variable'
			entt1.name = tk[0]
			entt1.variable.offset = compute_offset()
			new_entity(ennt1)
			tk = lex()
			
			while(tk[0] == koma_tk):
				tk = lex()
				
				if(tk[0] == id_tk):
					entt1 = Entity()
					entt1.type = 'Variable'
					entt1.name = tk[0]
					entt1.variable.offset = compute_offset()
					new_entity(ennt1)
					tk = lex()
					
				else:
					print("ERROR: Den yparxei komma prin to id H yparxoun 2 h parapanw id xwris komma metaksy tous", line)
					exit(-1)
		return
		
	def subprograms():
		global tk
		while(tk[0] == procedure_tk or tk[0] == function_tk ):  # koitame ena level pio katw
			
			subprogram()
			
		return
		
		
	def subprogram():
		global tk
		
		if(tk[0]==procedure_tk):
			tk=lex()

			if(tk[0]==id_tk):
				name=tk[1]
				
				entt2 = Entity()
				entt2.type = 'Subprogram'
				entt2.name = name
				entt2.subprogram.type = 'Procedure'
				new_entity(entt2)
				tk = lex()
				
				funcbody(name, 0 )  # 0, gt den einai function
			else:
				print("ERROR: Perimenoume to id meta to procedure ", line)
				exit(-1)
		elif(tk[0]== function_tk):
			tk = lex()

			name = tk[1]
			if(tk[0]==id_tk):
				name=tk[1]
				
				entt2 = Entity()
				entt2.type = 'Subprogram'
				entt2.name = name
				entt2.subprogram.type = 'Function'
				new_entity(entt2)
				tk = lex()

				
				funcbody(name , 1) 	# 1 gt einai function
			else:
				print("ERROR: Perimenoume to onoma function ",line)
				exit(-1)
		return
		
	def funcbody(blockName,isFunc):
		global tk
		formalpars()
		if(tk[0] == anoigma_block_tk):
			tk = lex()

			block(blockName , -1)    
			if(tk[0] == kleisimo_block_tk):
				tk = lex()

			else:
				print("ERROR: Den exei kleisei to block meta to formalpars", line)
				exit(-1)
		else:
			print("ERROR: Den exei ginei anoigma block gia to formalpars", line)
			exit(-1)
		return
		
		
	def formalpars():
		global tk
		
		if(tk[0] == arist_parenthesi_tk):
			tk = lex()
			
			formalparlist()
			
			if(tk[0] == deksia_parenthesi_tk):
				tk = lex()
				
			else:
				print("ERROR: Den kleinei h parenthesi sthn formalpars",line)
				exit(-1)
		else:
			print("ERROR: Den anoigei h parenthesi sthn formalpars", line)
			exit(-1)
		return
		
		
	def formalparlist():
		global tk
		
		formalparitem()
		
		while(tk[0] == koma_tk):
			tk  = lex()
			
			if(tk[0] == in_tk or tk[0] == inout_tk):
				
				formalparitem()
				
		return
		
	def formalparitem():
		global tk
		
		if(tk[0] == in_tk):
			tk = lex()
			
			if(tk[0]== id_tk):
				arg1 = Argument()
				arg1.name = tk[0]
				arg1.parMode = 'cv'
				new_argument(arg1)
				
				tk = lex()
				
			else:
				print("ERROR: Perimenei kanonika onoma metavlitis meta to 'in' ", line)
				exit(-1)
		elif(tk[0] == inout_tk):
			tk = lex()
			
			if(tk[0] == id_tk):
				arg1 = Argument()
				arg1.name = tk[0]
				arg1.parMode = 'ref'
				new_argument(arg1)
				
				tk = lex()
				
			else:
				print("ERROR: Perimenei kanonika onoma metavlitis meta to 'inout' ", line)
				exit(-1)
			
		return
			
			
	def statements():
		global tk
		
		if(tk[0] == anoigma_block_tk):
			tk = lex()
			
			statement()
			
			while(tk[0] == erwtimatiko_tk):
				tk = lex()
				
				statement()
				
			if(tk[0] == kleisimo_block_tk):
				tk = lex()
				
			else:
				print("ERROR: Den kleinei to block sta statements", line)
				exit(-1)
		else:
			
			statement()   # epeidh exei OR edw kalw thn statement
			
		return
		
		
	def statement():
		global tk
		
		if(tk[0]==id_tk):
			assignment_stat()
		elif(tk[0]==if_tk):
			if_stat()
		elif(tk[0]==while_tk):
			while_stat()
		#elif(tk[0]==doublewhile_tk):
			#doublewhile_stat()
		#elif(tk[0] == loop_tk):
			#loop_stat()
		#elif(tk[0]==exit_tk):
			#exit_stat()
		elif(tk[0]==forcase_tk):
			forcase_stat()
		#elif(tk[0] == incnase_tk):
			#incase_stat()
		elif(tk[0]==call_tk):
			call_stat()
		elif(tk[0]==return_tk):
			return_stat()
		elif(tk[0]==input_tk):
			input_stat()
		elif(tk[0]==print_tk):
			print_stat()
		else:
			print("ERROR: Mi apodekti entoli", line)
			exit(-1) 
		return
			
	
	
	def assignment_stat():
		#S-> id := E{P1};

		global tk, temp, flag
		
		id1 = tk[1]  #edw fortwnei to 1o
		tk = lex() #to epomeno
		if(tk[0] == anathesi_tk):
			tk = lex()
			Eplace = expression()
			#P1
			if(flag ==1):
				genQuad(':=', temp, '_', id1)
				flag =0
				
			else:
				genQuad(':=', Eplace, '_',id1)
		else:
			print("ERROR: Prepei na yparxei to symvolo anathesis meta to onoma tis metavlitis.", line)
			exit(-1)
		return


	def if_stat():
		'''
			S -> if B then {P1} S1{P2}TAIL{P3}
		'''

		global tk

		tk = lex()
		if(tk[0] == arist_parenthesi_tk):
			tk = lex()
			
			B = condition()
			
			if(tk[0]== deksia_parenthesi_tk):
				tk = lex()
				if(tk[0]== then_tk):
					tk = lex()
					#P1
					backPatch(B[0], nextQuad())
					statements()    #S1
					#P2
					ifList = makeList(nextQuad())
					genQuad('jump','_','_','_')
					backPatch(B[1],nextQuad())   #edw teleiwnei h {P2}
					elsepart()
					#P3
					backPatch(ifList, nextQuad())
					
				else:
					print("ERROR: Den exei then mesa sthn IF", line)
					exit(-1)
			else:
				print("ERROR: Den kleinei h parenthesi stin synthiki ths IF", line)
				exit(-1)
		else:
			print("ERROR: Den exei anoiksei parenthesi stin synthiki tis IF", line)
			exit(-1)
		Strue = B[0]
		Sfalse = B[1]
		return Strue, Sfalse
		
		
	def elsepart():
		'''
			TAIL -> else S2 | TAIL -> ε
		'''	
		global tk
	
		if(tk[0] == else_tk):
			tk = lex()
			
			statements()  #S2
			
		return 
		
		
	def while_stat():
		'''
			S -> while {P1} B do {P2} S1 {P3}
		'''
		global tk
		tk = lex()
		if(tk[0] == arist_parenthesi_tk):
			tk = lex()
			#P1
			Bquad = nextQuad()
			B = condition()
			
			if(tk[0] == deksia_parenthesi_tk):
				tk = lex()
				#P2
				backPatch(B[0], nextQuad())
				#tk = lex()
				statements()
				#P3
				genQuad('jump','_','_',Bquad)
				backPatch(B[1], nextQuad())
			else:
				print("ERROR: Den exei kleisei swsta h parenthesi stin synthiki tis WHILE", line)
				exit(-1)
		else:
			print("ERROR: Den exei anoiksei parenthesi sthn synthiki tis WHILE",line)
			exit(-1)
		SWtrue = B[0]
		SWfalse = B[1]
		return SWtrue, SWfalse
	
	
	def forcase_stat():
		'''
			forcase
			  ( when (<condition>) : <statements>)*
			  default: <statements>
		'''	  
		''' <forcase_stat>::= forcase {P0}
				 (when (B):{P1} S{P2} )*
				 default:S
		'''		 
		global tk
		if(tk[0] == forcase_tk):
			tk = lex()

			#P0
			q=nextQuad()
			while(tk[0] == when_tk):
				tk = lex()

				if(tk[0] == arist_parenthesi_tk):
					tk = lex()
					B=condition()
					if(tk[0] == deksia_parenthesi_tk):
						tk = lex()

						if(tk[0] == anwkatw_teleia_tk):
							tk = lex()

							#{P1}
							backPatch(B[0],nextQuad())
							statements()  #statements()
							#{P2}
							genQuad("jump","_","_",q)  #q apo to {P0}
							backPatch(B[1],nextQuad())
						else:
							print("ERROR: Den yparxei anw katw teleia sthn FORECASE", line)
							exit(-1)
					else:
						print("ERROR: Den yparxei deksia parenthesi sthn FORECASE", line)
						exit(-1)
				else:
					print("ERROR: Den yparxei aristeri parenthsi sthn FORECASE", line)
					exit(-1)
			#default		
			if(tk[0] == default_tk):
				tk = lex()

				if(tk[0] == anwkatw_teleia_tk):
					tk = lex()

					statements()

					
				else:
					print("ERROR: Den yparxei anw katw teleia sthn DEFAULT ths FORECASE",line)
					exit(-1)
			else:
				print("ERROR: Den ksekinaei swsta h DEFAULT ths FORECASE", line)
				exit(-1)
		else:
			print("ERROR: Den ksekinaei swsta h FORECASE", line)
			exit(-1)
		return
		

		
	def return_stat():
		#RS-> return (E) {P1}
		global tk
		tk = lex()
		
		Eplace = expression()
		genQuad('retv', Eplace, '_','_')

		return
		
	def call_stat():
		global tk

		if(tk[0] == call_tk):
			tk = lex()
			id2 = tk[1]
			if(tk[0] == id_tk):
				tk = lex()
				
				actualpars(0, id2)
				
			else:
				print("ERROR: Den yparxei id sthn CALL", line)
				exit(-1)
		else:
			print("ERROR: Den arxizei swsta h CALL",line)
			exit(-1)
		
		return
		
	def print_stat():
		#S-> print (E) {P2}
		global tk
		
		tk = lex()
		if(tk[0]== arist_parenthesi_tk):
			tk = lex()
			Eplace = expression()
			if(tk[0] == deksia_parenthesi_tk):
				tk = lex()	#P2
				genQuad('out', Eplace, '_', '_')
			else:
				print('ERROR: Expected ")"', line)
				exit(-1)
		else:
			print('ERROR: Expected "("', line)
			exit(-1)
		return
		
	def input_stat():
		#S-> input (id) {P1}
		global tk
		tk = lex()
		if(tk[0]== arist_parenthesi_tk):
			tk = lex()
			IDplace = expression()
			if(tk[0] == deksia_parenthesi_tk):
				tk = lex()	#P2
				genQuad('inp', IDplace, '_', '_')
			else:
				print('ERROR: Expected ")"', line)
				exit(-1)
		else:
			print('ERROR: Expected "("', line)
			exit(-1)
		return
		
	def actualpars(flag, idNAME):
		global tk, temp
		
		if(tk[0] == arist_parenthesi_tk):
			tk = lex()
			
			actualparlist()
			
			if(tk[0] == deksia_parenthesi_tk):
				tk = lex()
				if(flag == 1):
					w = newTemp()
					genQuad('par', w, 'RET', '_')
					genQuad('call', idNAME, '_','_')
					temp = w
				else:
					genQuad('call', idNAME,'_','_')
				return
			else:
				print("ERROR: Den kleinei h parenthesi stin ACTUALPARS",line)
				exit(-1)
		else:
			print("ERROR: Den anoigei parenthesi stin ACTUALPARS", line)
			exit(-1)
		return
		
		
	def actualparlist():
		global tk
		
		actualparitem()
		
		while(tk[0] == koma_tk):
			tk  = lex()
			
			actualparitem()
			
		return
		
	def actualparitem():
		global tk
		
		if(tk[0] == in_tk):
			tk = lex()
			exp = expression()
			genQuad('par', exp, 'CV', '_')
		elif(tk[0] == inout_tk):
			tk = lex()
			if(tk[0] == id_tk):
				genQuad('par', tk[1], 'REF','_')
				tk = lex()
			else:
				print("ERROR: Perimenei kanonika onoma metavlitis meta to 'inout' ", line)
				exit(-1)
		return
		
		
	def condition():
		'''
			B -> Q1 {P1}(or {P2} Q2{P3})*
		'''
		global tk
		trueC = []
		falseC = []
		Q1 = boolterm()
		#P1
		trueC = Q1[0]
		falseC = Q1[1]
		while(tk[0]==or_tk):
			tk=lex()
			#P2
			backPatch(falseC, nextQuad())
			Q2 = boolterm()
			#P3
			trueC = merge(trueC, Q2[0])
			falseC = Q2[1]
		return trueC, falseC
		
		
	def boolterm():
		'''
			Q -> R1{P1}(and{P2}R2{P3})*
		'''
		global tk
		Qtrue = []
		Qfalse = []
		R1 = boolfactor()
		#P1
		Qtrue = R1[0]
		Qfalse = R1[1]
		
		while(tk[0]==and_tk):
			tk=lex()
			#P2
			backPatch(Qtrue, nextQuad())
			R2 = boolfactor()
			#P3
			Qfalse = merge(Qfalse, R2[1])
			Qtrue = R2[0]
		return Qtrue, Qfalse
		
	def boolfactor():
		'''
			R -> [B] {P1}
		'''
		global tk
		Rtrue = []
		Rfalse = []
		Eplace1, Eplace2, relop = '', '', ''
		
		if(tk[0]==not_tk):
			'''
				R-> not [B] {P1}
			'''
			tk=lex()
			if(tk[0] == arist_agkili_tk):
				tk=lex()
				C =condition()										
				if(tk[0] == deksia_agkili_tk):
					tk=lex()
					#P1
					Rtrue = C[1]					
					Rfalse = C[0]					
				else:
					print('error: Expected "]" after condition. \tLine> %d:%d' % (line, position))
					exit(1)
			else:
				print('error: Expected "[" after "not". \tLine> %d:%d' % (line, position))
				exit(1)
		elif(tk[0] == arist_agkili_tk):
			'''
				R-> [B] {P1}
			'''
			tk=lex()
			C =condition()							
			if(tk[0]== deksia_agkili_tk):
				tk=lex()
				#P1
				Rtrue = C[0]						
				Rfalse = C[1]						
			else:
				print('error: Expected "]" after condition. \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			'''
				R-> E1 relop E2 {P1}
			'''
			Eplace1 =expression()	

			relop = relational_oper()

			Eplace2 =expression()
			
			#P1
			Rtrue=makeList(nextQuad())
			genQuad(relop, Eplace1, Eplace2, '_')	
			Rfalse=makeList(nextQuad())
			genQuad('JUMP', '_', '_', '_')			
		return Rtrue, Rfalse
		
		
	def expression():
		#E-> T1 (+- T2 {P1})* {P2}
		global tk
		optional_sign()
		T1place = term()

		while(tk[0] == plus_tk or tk[0] == minus_tk):
			plusORminus = add_oper()
			T2place = term()
			w = newTemp()	#P1
			genQuad(plusORminus, T1place, T2place, w)
			T1place = w
		Eplace = T1place	#P2
		return	Eplace
		
		
		
	def term():
		global tk
		#T-> F1 (mulOper F2 {P1})* {P2}
		
		F1place = factor()
		
		while(tk[0] == multiply_tk or tk[0] == divide_tk ):
			mulORdiv = mul_oper()
			F2place = factor()
			w = newTemp()	#P1
			genQuad(mulORdiv, F1place, F2place, w)
			F1place = w
		Tplace = F1place	#P2
		return Tplace
		
		
	def factor():
		global tk
		
		if(tk[0]==num_tk):
			factor1 = tk[1]
			tk = lex()
		elif(tk[0]==arist_parenthesi_tk):
			tk = lex()
			Eplace = expression()
			if(tk[0] == deksia_parenthesi_tk):
				factor1 = Eplace
				tk = lex()
				
			else:
				print("ERROR: Theloume dexia parenthesi ')' meta to expression stin FACTOR ",line)
				exit(-1)
		elif(tk[0] == id_tk):
			factor1 = tk[1]
			tk = lex()
			idtail(factor1)	#na valw orisma to factor1
			
		else:
			print("ERROR: Theloume constant h expression h variable stin FACTOR",line)
			exit(-1)
		
		return factor1
		
	
	def idtail(idNAME):
		global tk, flag
		
		if(tk[0] == arist_parenthesi_tk ):
			flag =1
			actualpars(1, idNAME)
		return
		
		
	def relational_oper():
		global tk 

		rel=tk[1]
		
		if(tk[0]==equal_tk):
			tk = lex()
			
		elif(tk[0]==lessthan_tk):
			tk = lex()
			
		elif(tk[0]==lessORequal_tk):
			tk = lex()
			
		elif(tk[0]==diaforo_tk):
			tk = lex()
			
		elif(tk[0]== greaterthan_tk):
			tk = lex()
			
		elif(tk[0]==greaterORequal_tk):
			tk = lex()
			
		else:
			print("ERROR: Leipei = h < h <= h <> h >= h > ",line)
			exit(-1)
		return rel
		
	def add_oper():
		global tk 
		
		if(tk[0]==plus_tk):
			tk = lex()

			return '+'

		elif(tk[0]==minus_tk):
	
			tk = lex()

			return '-'
		

	def mul_oper():
		global tk 

		
		if (tk[0] == multiply_tk):
			tk = lex()

			return '*'
		elif (tk[0] == divide_tk):
			tk = lex()

			return '/'

	def optional_sign():
		global tk

		
		if(tk[0] == plus_tk or tk[0] == minus_tk):
			
			add_oper()
			
		return

	program()
	print(' \n ________________')
	print('*_____OK_END_____*')
	return

'''
#########################################################
Paragwgi arxeiou .c kai .init
#########################################################
'''
def intCode(intfFILE):
	for i in range(len(quadlist)):
		quad = quadlist[i]
		intfFILE.write(str(quad[0]))
		intfFILE.write(":  ")
		intfFILE.write(str(quad[1]))
		intfFILE.write("  ")
		intfFILE.write(str(quad[2]))
		intfFILE.write("  ")
		intfFILE.write(str(quad[3]))
		intfFILE.write("  ")
		intfFILE.write(str(quad[4]))
		intfFILE.write("\n")

def cCode(cFILE):
	global tempList
	
	if(len(tempList)!=0):
		cFILE.write("int ")

	for i in range(len(tempList)):
		cFILE.write(tempList[i])
		
		if(len(tempList) == i+1):
			cFILE.write(";\n\n\t")
		else:
			cFILE.write(",")
	
	for j in range(len(quadlist)):
		if(quadlist[j][1] == 'begin_block'):
			cFILE.write("L_"+str(j+1)+":\n\t")
		elif(quadlist[j][1] == ":="):
			cFILE.write("L_"+str(j+1)+": "+ quadlist[j][4]+"="+quadlist[j][2]+";\n\t")
		elif(quadlist[j][1] == "+"):
			cFILE.write("L_"+str(j+1)+": "+ quadlist[j][4]+"="+quadlist[j][2]+"+"+quadlist[j][3]+";\n\t")
		elif(quadlist[j][1] == "-"):
			cFILE.write("L_"+str(j+1)+": "+ quadlist[j][4]+"="+quadlist[j][2]+"-"+quadlist[j][3]+";\n\t")
		elif(quadlist[j][1] == "*"):
			cFILE.write("L_"+str(j+1)+": "+ quadlist[j][4]+"="+quadlist[j][2]+"*"+quadlist[j][3]+";\n\t")
		elif(quadlist[j][1] == "/"):
			cFILE.write("L_"+str(j+1)+": "+ quadlist[j][4]+"="+quadlist[j][2]+"/"+quadlist[j][3]+";\n\t")
		elif(quadlist[j][1] == "JUMP"):
			cFILE.write("L_"+str(j+1)+": "+"goto L_"+str(quadlist[j][4])+ ";\n\t")
		elif(quadlist[j][1] == "<"):
			cFILE.write("L_"+str(j+1)+": "+"if ("+quadlist[j][2]+"<"+quadlist[j][3]+") goto L_"+str(quadlist[j][4])+";\n\t")
		elif(quadlist[j][1] == ">"):
			cFILE.write("L_"+str(j+1)+": "+"if ("+quadlist[j][2]+">"+quadlist[j][3]+") goto L_"+str(quadlist[j][4])+";\n\t")
		elif(quadlist[j][1] == ">="):
			cFILE.write("L_"+str(j+1)+": "+"if ("+quadlist[j][2]+">="+quadlist[j][3]+") goto L_"+str(quadlist[j][4])+";\n\t")
		elif(quadlist[j][1] == "<="):
			cFILE.write("L_"+str(j+1)+": "+"if ("+quadlist[j][2]+"<="+quadlist[j][3]+") goto L_"+str(quadlist[j][4])+";\n\t")
		elif(quadlist[j][1] == "<>"):
			cFILE.write("L_"+str(j+1)+": "+"if ("+str(quadlist[j][2])+"!="+str(quadlist[j][3])+") goto L_"+str(quadlist[j][4])+";\n\t")
		elif(quadlist[j][1] == "="):
			cFILE.write("L_"+str(j+1)+": "+"if ("+quadlist[j][2]+"=="+quadlist[j][3]+") goto L_"+str(quadlist[j][4])+";\n\t")
		elif(quadlist[j][1] == "out"):
			cFILE.write("L_"+str(j+1)+": "+"printf(\""+quadlist[j][2]+"= %d\", "+quadlist[j][2]+");\n\t")
		elif(quadlist[j][1] == 'halt'):
			cFILE.write("L_"+str(j+1)+": {}\n\t")
	
def files():
	intFILE = open('intFILE.int', 'w')
	cFILE = open('cFILE.c', 'w')
	
	cFILE.write("int main(){\n\t")

	syntax_an(cFILE)
	intCode(intFILE)
	cCode(cFILE)
	
	cFILE.write("\n}")
	
	#Close open files
	cFILE.close()
	intFILE.close()
	
files()






























