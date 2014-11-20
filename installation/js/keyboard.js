function focusOnLastChar(id) {
	var elem = document.getElementById(id);
	var elemLen = elem.value.length;
	elem.selectionStart = elemLen;
	elem.selectionEnd = elemLen;
	elem.focus();
}

function Key(normal, upper) {
          this.normal = normal;
          this.upper = upper;
          this.GetNormal = GetKeyNormal;
          this.GetUpper = GetKeyUpper;
     }
     function GetKeyNormal() {
          return this.normal;
     }
     function GetKeyUpper() {
          return this.upper;
     }

     var width = 14;
     var height = 4;
     var keys_lower = Array('OK', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '�', '�', '<--',
                            '~', 'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', '�', '+', '~', 
                            '^^', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '�', '�', '#', '^^',
                            '^', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', 'SPACE', '^', '^' );
     var keys_upper = Array('OK', '!', '"', '�', '$', '%', '&', '/', '(', ')', '=', '=', '`', '<--',
                            '~', 'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', '�', '*', '~',
                            '^^', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '�', '�', "'", '^^',
                            '^', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_', 'SPACE', '^', '^' );
     var keys = [];
     var upperKeyIds = [ 28, 41];
     var upperOnceKeys = [ 42, 54, 55 ]; 
     var deleteKeys = [ 13 ];
     var okKey = 0;
     var isUpper = false;
     var isUpperOnce = false; 
     var destinationId = "null";     
     var spaceKeys = [ 53 ];
     function keyboardSetup(destid) {
          /* keys = [];
          destinationId = destid;
          for(var i = 0; i <= keys_upper.length; i++) {
                keys.push(new Key(keys_lower[i], keys_upper[i]));
          }
          document.getElementById("keyboard").style.display = '';
          draw();*/
     }



     function draw() {
          document.getElementById("keyboard").innerHTML = ' ';
          document.getElementById("keyboard").innerHTML += '<div id="keyboardRow">';
          for(var i = 0; i< keys.length-1; i++) {
               if(isUpper==true) {
                    document.getElementById("keyboard").innerHTML += "<button onclick=\"WasClicked("+i+");\">"+keys[i].GetUpper()+"</button>";
                    
               } else {
                    document.getElementById("keyboard").innerHTML += "<button onclick=\"WasClicked("+i+");\">"+keys[i].GetNormal()+"</button>";
               } 
 
               if (i % width == 13) {
                    document.getElementById("keyboard").innerHTML += '</div><br>';
                    document.getElementById("keyboard").innerHTML += '<div id="keyboardRow">';
               }
          }
          document.getElementById("keyboard").innerHTML += '</div>';
     }

     function WasClicked(id) {
          if(id==okKey) {
               document.getElementById("keyboard").style.display = 'none';
               return;
          }
          else if(deleteKeys.indexOf(id)!=-1) {
               var content = document.getElementById(destinationId).value;
               document.getElementById(destinationId).value = content.substr(0, content.length-1);
          } 
          else if(spaceKeys.indexOf(id)!=-1) {
		document.getElementById(destinationId).value += " ";
	   }
          else if(upperKeyIds.indexOf(id)==-1 && upperOnceKeys.indexOf(id)==-1) {
                    if(isUpper===true) {
                              document.getElementById(destinationId).value += keys[id].GetUpper();
                              if(isUpperOnce===true) {
                                        isUpper = false;
                                        usUpperOnce = false;
                              }
                              
                    } else {
                          document.getElementById(destinationId).value += keys[id].GetNormal();
                    }
          } else {
               if(upperKeyIds.indexOf(id)!=-1) {
                    isUpper = !isUpper;
                    isUpperOnce = false;
               } else {
                    isUpper = !isUpper;
                    isUpperOnce = true;
               }
          }
		  document.getElementById(destinationId).onkeyup();
          draw(); 
		  focusOnLastChar(destinationId);
   }
   
function HideKeyboard() {
	 document.getElementById("keyboard").style.display = 'none';
}