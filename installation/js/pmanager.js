function DrawManagerScreen() {
	document.getElementById('content').style.display = "";
	document.getElementById('newProductContent').style.display = "none";
	//Draw current product selection
	document.getElementById('sidebarOutput').innerHTML = "";
	document.getElementById('content').innerHTML = "";
	if (isParentActive===false) {
		for(var i = 0; i<products.length;i++) {
			if(products[i].hasParent===false) {
				document.getElementById('content').innerHTML += "<div id=\"product\" onclick=\"ProductSelectedManager("+i+")\">"+products[i].name+" - "+products[i].price+"</div>";
			}
		}
	} else {
		for(var i = 0; i<products.length;i++) {
			if(products[i].hasParent===true && products[i].parent == ActiveParent) {
				document.getElementById('content').innerHTML += "<div id=\"product\" onclick=\"ProductSelectedManager("+i+")\">"+products[i].name+" - "+products[i].price+"</div>";
			}
		}
	}
	document.getElementById('content').innerHTML += "<div id=\"product\" onclick=\"ProductManagerAddNew()\">Add New...</div>";
}

function ProductSelectedManager(id) {
	
	//find out if there are objects with this object as parent
	var hasChildren = false;
	for(var i = 0; i<products.length;i++) {
		if(products[i].parent == products[id].realId) {
			hasChildren = true;
			break;
		}
	}
	
	isParentActive = true;
	ActiveParent = products[id].realId;
	
	document.getElementById('pmanager_name').value = products[id].name;
	document.getElementById('pmanager_price').value = products[id].price;
	
	DrawManagerScreen();
}

function ProductManagerUpdate() {
	var getText = "?pId="+ActiveParent+"&name="+document.getElementById('pmanager_name').value+"&price="+document.getElementById('pmanager_price').value;
	document.location.href = "/system/api/changeProduct.html"+getText;
}

function ProductManagerDelete() {
	var getText = "?pId="+ActiveParent+"&name="+document.getElementById('pmanager_name').value+"&price="+document.getElementById('pmanager_price').value+"&isDeleted=true";
	document.location.href = "/system/api/changeProduct.html"+getText;
}

function ProductManagerBack()
{
	isParentActive = false;
	ActiveParent = -1;
	document.getElementById('pmanager_name').value = "";
	document.getElementById('pmanager_price').value = "";
	DrawManagerScreen();
}

function ProductManagerAddNew()
{
	document.getElementById('content').style.display = "none";
	document.getElementById('newProductContent').style.display = "";
	
	//document.getElementById('content').innerHTML = contentString;
}

function ProductManagerAddNewFinish()
{
	strBuyable = "true";
	if(document.getElementById('pmanager_new_isBuyable').checked == false) {
		strBuyable = "false";
	}
	strIsChild = "false";
	if(isParentActive==true) {
		strIsChild = "true";
	}
	var getText = "?name="+document.getElementById('pmanager_new_name').value+"&price="+document.getElementById('pmanager_new_price').value+"&isBuyable="+strBuyable+"&hasParent="+strIsChild+"&parent="+ActiveParent;
	document.location.href = "/system/api/addProduct.html"+getText;
}
