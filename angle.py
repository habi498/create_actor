import math
PI = 3.1415926
def encode_angle( x ): # -3.14 < x < 3.14
    y = math.floor( x * 4096 * 4/PI + 32767 )
    h = hex(y);
    return [int(h[2:4],16),int(h[4:6],16)];
    
def decode_angle( w ): #eg.[127 255]
   return ( h(split(w))-32767 )*PI/4*1/pow(16,3); # 7f ff
def split( x ): #[7f]-->[7 f]
    a = math.floor(x[0]/16);
    b = x[0]%16
    c= [a, b]
    if( len(x) > 1 ):
        d = split( x[1:] );
        d.insert( 0, b );
        d.insert( 0, a );
        return d;
    else:
        return c;
def join( x ): #[7 f]-->[7f]
    length=len(x);
    if(length%2 == 1):
        x.append(0);
    c=[];
    for i in range(0, length, 2):
        y=x[i]*16+x[i+1];
        c.append(y);
    return c;
def h( x ): #[15 4 9 6] --> corresponding integer 16^3*15+16^2*4+16*9+6
    if(len(x) > 1):
        return x[0]* pow(16, len(x)-1) + h(x[1:]);
    else:
        return  x[0]

