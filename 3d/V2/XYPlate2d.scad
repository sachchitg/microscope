include <ISOThreadLeg.scad>

$fn=1000;
module plate(x,y){
       translate ([x,y]) { 
           difference() {
             square([100,100]);
               
            cx = 92.5;
            cy = 72.5;
            M3 = 3 + 0.15;
            M5 = 5 + 0.15;
            
           
            translate ([cx,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy-15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy-2*15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy-3*15]) {
                circle (d=M3, center=true);
            }
            
            translate ([100-cx,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([100-cx,cy-15]) {
                circle (d=M3, center=true);
            }
            
            translate ([100-cx,cy-2*15]) {
                circle (d=M3, center=true);
            }
            
            translate ([100-cx,cy-3*15]) {
                circle (d=M3, center=true);
            }
              
            
            dny = 50;
            dnx = 16.25+10;
            
           translate ([dnx,dny]) {
                circle (d=M5,center=true);
                }
                
           translate ([dnx+20,dny]) {
                circle (d=M5,center=true);
                }
            
            sy = dny-5;
            sx = dnx + 32.25;
                    
            translate ([sx,sy]) {
               circle (d=M3, center=true);
            }
            
            translate ([sx,sy+10]) {
                circle (d=M3, center=true);
            }
            
            translate ([sx+15,sy]) {
                circle (d=M3, center=true);
            }
            
            translate ([sx+15,sy+10]) {
                circle (d=M3, center=true);
            }
            
            
            }
        }
}

module stage(x,y){
       translate ([x,y]) { 
           difference() {
             square([100,100]);
               
            cx = 92.5;
            cy = 72.5;
            M3 = 3 + 0.15;
            M30 = 30 + 0.15;
           
            translate ([cx,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy-15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy-2*15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy-3*15]) {
                circle (d=M3, center=true);
            }
            
            translate ([100-cx,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([100-cx,cy-15]) {
                circle (d=M3, center=true);
            }
            
            translate ([100-cx,cy-2*15]) {
                circle (d=M3, center=true);
            }
            
            translate ([100-cx,cy-3*15]) {
                circle (d=M3, center=true);
            }
            
            translate ([50,50]) {
                circle (d=M30);
            }
            
            }
        }
}


plate(0,0);
plate(101,0);
plate(101,101);
plate(0,101);
