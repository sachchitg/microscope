$fn=100;
module plate(x,y){
       translate ([x,y,0]) { 
           difference() {
             cube([100,100,5]);
               
            cx = 92.5;
            cy = 72.5;
            
            M3 = 1.0155*3 + 0.2795;
            M5 = 1.0155*5 + 0.2795;
           
            translate ([cx,cy,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([cx,cy-15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([cx,cy-2*15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([cx,cy-3*15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([100-cx,cy,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([100-cx,cy-15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([100-cx,cy-2*15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([100-cx,cy-3*15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
              
            
            dny = 50;
            dnx = 16.25+10;
            
           translate ([dnx,dny,-20]) {
                cylinder (d=M5, h=100, center=true);
                }
                
           translate ([dnx+20,dny,-20]) {
                cylinder (d=M5, h=100, center=true);
                }
            
            sy = dny-5;
            sx = dnx + 32.25;
                    
            translate ([sx,sy,-20]) {
               cylinder (d=M3, h=100, center=true);
            }
            
            translate ([sx,sy+10,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([sx+15,sy,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([sx+15,sy+10,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            
            }
        }
}

module stage(x,y){
       translate ([x,y]) { 
           difference() {
             cube([100,100,5]);
               
            cx = 92.5;
            cy = 72.5;
            
            M3 = 1.0155*3 + 0.2795;
            M30 = 1.0155*30 + 0.2795;
           
            translate ([cx,cy,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([cx,cy-15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([cx,cy-2*15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([cx,cy-3*15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([100-cx,cy,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([100-cx,cy-15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([100-cx,cy-2*15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([100-cx,cy-3*15,-20]) {
                cylinder (d=M3, h=100, center=true);
            }
            
            translate ([50,50,-20]) {
                cylinder (d=M30, h=100, center=true);
            }
            
            }
        }
}



plate(0,0);
plate(105,0);
stage(105,105);
plate(0,105);

