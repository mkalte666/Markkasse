//Generated vars for the product selection
var pIds = [0,1,2,3,4,5];
var names = ["Sandwich", "Getr�nk", "Snack", "K�se", "Chester", "Allg�uer"];
var prices = [0.40, 0.50, 0.00, 0.00, 0.10, 0.10];
var pHasParent = [false, false, false, true, true, true];
var pShouldOutput = [true, true, true, false, true, true];
var parents = [-1, -1, -1, 0, 3, 3];

//Generated vars for the user selection
var RawUsers = ["Malte Kie�ling", "Robin Beckmeyer", "Max-Malte Hansen"];
var uIds = [0, 1, 10];
var uAbleToBuy = [true, true, false];
var debts = [1.50, 2.50, 10.98];

//user creation control
var ActiveUser = {};
var isNewUser = false;
var ActiveLetter = "A";
function user(uId, name, debt, ableToBuy) {
	this.uId = uId;
	this.name = name;
	this.debt = debt;
	this.ableToBuy = ableToBuy;
	this.letter = name[0].toUpperCase();
}

var users = [];
for(var i = 0; i<RawUsers.length; i++) {
	users.push(new user(uIds[i], RawUsers[i], debts[i], uAbleToBuy[i]));
}

//User Management
function DrawUserSelectoin() {
	document.getElementById('content').innerHTML = "";
	//Draw the normal letters as boxes for alphabetical ordering
	var beginChar = 65; //A
	var endChar = 65+26; //Z
	var buttons = "";
	for(var i = beginChar; i<endChar; i++) {
		var letter = String.fromCharCode(i);
		buttons += "<button onclick=\"UserLetterSet('"+letter+"')\">"+letter+"</button>";
	}
	document.getElementById('content').innerHTML += "<div id=\"userselection_buttons\">"+buttons+"</div>";
	
	//Draw the users from the selection after ordering alphabetical
	var lines = [];
	//alert(ActiveLetter);
	for(var i = 0; i < users.length; i++) {
		//alert(users[i].letter);
		if(users[i].letter == ActiveLetter) {
			if(users[i].ableToBuy===true) {
				lines.push("<!-- Sorthelper:"+users[i].name+"--><div id=\"userselection_name\" onclick=\"selectUser("+i+")\">"+users[i].name+"</div>");
			} else {
				lines.push("<!-- Sorthelper:"+users[i].name+"--><div id=\"userselection_name_blocked\">"+users[i].name+"</div>");
			}
		}
	}	
	lines.sort();
	lines.push("<div id=\"userselection_name\" onclick=\"addUser()\">Add New...</div>");
	userselection = "";
	for(var i = 0; i<lines.length; i++) {
		userselection += lines[i];
	}
	document.getElementById('content').innerHTML += "<div id=\"userselection\">"+userselection+"</div>";
}

function UserLetterSet(letter) {
	ActiveLetter = letter;
	DrawUserSelectoin();
}

function selectUser(id) {
	ActiveUser = users[id];
	document.getElementById("usernameOutput").innerHTML = "<div id=\"usernameText\" onclick=\"DrawUserSelectoin()\">"+ActiveUser.name+"</div>";
	isNewUser = false;
	DrawProductScreen();
}

function addUser() {
	document.getElementById("usernameOutput").innerHTML = "<input onclick=\"keyboardSetup('addUserInput');\" type=\"text\" id=\"addUserInput\" /><button onclick=\"addUserDone()\">OK</button>";
	keyboardSetup('addUserInput');
}

function addUserDone() {
	DrawProductScreen();
	newUsername = document.getElementById("addUserInput").value;
	isNewUser = true;
	ActiveUser = new user(-1, newUsername, 0.0, true);
	document.getElementById("usernameOutput").innerHTML = "<div id=\"usernameText\" onclick=\"DrawUserSelectoin()\">"+ActiveUser.name+"</div>";
	HideKeyboard(); 
}

function SerializeUserselection()
{
	output = "&";
	if(isNewUser===true) {
		output += "newUser=true&";
	} else {
		output += "newUser=false&";
	}
	
	output += "uid="+ActiveUser.uId+"&";
	output += "name="+ActiveUser.name+"&";
	return output;
}
//Product Management


function Product(realId, name, price, hasParent, parent, shouldOutput) {
	this.realId = realId;
	this.name = name;
	this.price = price;
	this.hasParent = hasParent;
	this.parent = parent;
	this.shouldOutput = shouldOutput;
}

function OutputProduct(product, virtualId) {
	this.subs = [];
	this.product = product;
	this.id = virtualId;
}

var products = [];
var ActiveParent = -1;
var isParentActive = false;
var OutputCollection = [];
var OutputCollectionCounter = 0;
var ActiveOutput = 0;

for (var i = 0; i<pIds.length;i++) {
	products.push(new Product(pIds[i], names[i], prices[i], pHasParent[i], parents[i], pShouldOutput[i]));
}



function DrawProductScreen() {
	//Draw current product selection
	document.getElementById('sidebarOutput').innerHTML = "";
	document.getElementById('content').innerHTML = "";
	if (isParentActive===false) {
		for(var i = 0; i<products.length;i++) {
			if(products[i].hasParent===false) {
				document.getElementById('content').innerHTML += "<div id=\"product\" onclick=\"ProductSelected("+i+")\">"+products[i].name+"</div>";
			}
		}
	} else {
		for(var i = 0; i<products.length;i++) {
			if(products[i].hasParent===true && products[i].parent == ActiveParent) {
				document.getElementById('content').innerHTML += "<div id=\"product\" onclick=\"ProductSelected("+i+")\">"+products[i].name+"</div>";
			}
		}
	}
	
	//Draw the sidebar with all the information
	for(var i = 0; i < OutputCollection.length; i++) {
		if(OutputCollection[i].product.shouldOutput===true) {
			document.getElementById('sidebarOutput').innerHTML += "<div id=\"Output\"><div id=\"texthelper\" onclick=\"SwitchFocus("+i+")\">"+OutputCollection[i].product.name+"</div><button onclick=\"RemoveOutput("+i+")\">X</button></div>";
			}
		for(var j = 0; j < OutputCollection[i].subs.length; j++) {
			if(OutputCollection[i].subs[j].product.shouldOutput===true) {
				document.getElementById('sidebarOutput').innerHTML += "<div id=\"Suboutput\">"+OutputCollection[i].subs[j].product.name+"<button onclick=\"RemoveSubOutput("+i+","+j+")\">X</button></div>";
			}
		}
		document.getElementById('sidebarOutput').innerHTML += "<br>";
	}
}

function SwitchFocus(id) {
	ActiveOutput = id;
	isParentActive = true;
	//switch from db-style to normal style
	for(var i=0; i < products.length; i++) {
		if (products[i].realId==OutputCollection[id].product.realId) {
			ActiveParent = i;
			break;
		}
	}
	
	DrawProductScreen();
}

function RemoveOutput(id) {
	OutputCollection.splice(id, 1);
	ProductBack();
}

function RemoveSubOutput(id, subid) {
	OutputCollection[id].subs.splice(subid, 1);
	DrawProductScreen();
}

function ProductSelected(id) {
	
	//add to outtree
	newProduct = new OutputProduct(products[id], OutputCollectionCounter);
	if(isParentActive===true) {
		OutputCollection[ActiveOutput].subs.push(newProduct);
		OutputCollectionCounter++;
	} else {
		OutputCollection.push(newProduct);
		ActiveOutput = OutputCollection.length-1;
		//set stuff for next round
	}
	OutputCollectionCounter++;
	//find out if there are objects with this object as parent
	var hasChildren = false;
	for(var i = 0; i<products.length;i++) {
		if(products[i].parent == id) {
			hasChildren = true;
			break;
		}
	}
	
	if(hasChildren===true) {
			isParentActive = true;
			ActiveParent = id;
	}
	
	DrawProductScreen();
}

function ProductBack() {
	isParentActive = false;
	ActiveParent = -1;
	DrawProductScreen();
}

function SerializeProductselection() {
	output = "products=";
	for(var i = 0; i<OutputCollection.length;i++) {
		if(OutputCollection[i].product.shouldOutput==true) {
			output += "+p" + OutputCollection[i].product.realId;
		}
		for(var j = 0; j < OutputCollection[i].subs.length; j++) {
			if(OutputCollection[i].subs[j].product.shouldOutput==true) {
				output += "+sp" + OutputCollection[i].subs[j].product.realId;
			}
		}
	}
	output += "&";
	return output;
} 

//Final stuff for checking, money-input and output and blah
var WasPaied = true;

function CreateGET() {
	output = "?"+SerializeProductselection()+SerializeUserselection();
	if(WasPaied===true) {
		output += "&wasPaied=true";
	} else {
		output += "&wasPaied=false";
	}
	return output;
}

function DrawFinishScreen(inputmoney) {
	var ToPay = 0.0;
	for(var i = 0; i<OutputCollection.length;i++) {
		if(OutputCollection[i].product.shouldOutput==true) {
			ToPay += OutputCollection[i].product.price;
		}
		for(var j = 0; j < OutputCollection[i].subs.length; j++) {
			if(OutputCollection[i].subs[j].product.shouldOutput==true) {
				ToPay += OutputCollection[i].subs[j].product.price;
			}
		}
	}
	
	output = "<div id=\"finishOrder_toPay\">"+(ToPay*100).toFixed()+" cent </div>";
	output += "<input type=\"text\" id=\"finishOrder_input\" onkeyup=\"UpdateFinishScreen()\" value=\""+(inputmoney*100).toFixed()+"\"\"/>";
	
	if((inputmoney-ToPay).toFixed() >= 0) {
		output += "<button id=\"finishOrder_button\" onclick=\"finishOrder()\">Finish</button>";
		output += "<div id=\"finishOrder_change\">Change: "+(inputmoney*100-ToPay*100).toFixed()+" cent</div>";
	} else {
		output += "<div id=\"finishOrder_changerror\">Still needed: "+(ToPay*100-inputmoney*100).toFixed()+" cent</div>";
	}
	output += "<button id=\"finishOrder_button\" onclick=\"finishOrderWithoutCash()\">Anschreiben</button>";
	document.getElementById('content').innerHTML = output;
	keyboardSetup('finishOrder_input');
}

function UpdateFinishScreen() {
	var intext = document.getElementById('finishOrder_input').value;
	inputmoney = parseFloat(intext)/100;
	if(isNaN(inputmoney)) {
		DrawFinishScreen(0);
	} else {
		DrawFinishScreen(inputmoney);
	}
	
	focusOnLastChar('finishOrder_input');
	
}

function finishOrder() {
	alert(CreateGET());
	document.location.href="/system/placeOrder.html"+CreateGET();
}

function finishOrderWithoutCash() {
	WasPaied=false;
	finishOrder();
}

function ProductCancel() {
	document.location.href="/system/home.html";
}