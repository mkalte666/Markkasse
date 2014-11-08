function usernameById(id)
{
	for(var i = 0; i<users.length; i++) {
	        if (users[i].uId == id) {
	                return users[i].name;
		}
        }
}

function productnameById(id)
{
	for(var i = 0; i<products.length; i++) {
            if (products[i].realId == id) {
                return products[i].name;
	        }
        }
}

function DrawPendingOrders(destination, drawOnlyOverview, maxorders, maxproducts)
{
	orderString = "";
	
	for(var i = 0; i<pendingOrderIds.length && i<maxorders; i++) {
		orderString += "<div id=\"singlePendingOrder\">"
		orderString += "<div id=\"PendingOrderUser\">"+usernameById(pendingOrderUIds[i])+"</div>";
		for(var j = 0; j<pendingOrderProducts[i].length && j<maxproducts;j++) {
			orderString += "<div id=\"PendingOrderProduct\">"+productnameById(pendingOrderProducts[i][j])+"</div>";
		}
		orderString += "<button id=\"FinishPendingOrderButton\">"+"Done"+"</button>";
		orderString += "<button id=\"CancelPendingOrderButton\">"+"Cancel"+"</button>";
		orderString += "</div>"
	}
		    
	document.getElementById(destination).innerHTML += orderString;
}
