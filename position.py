import math
def decode_coord( wstr ):#wstr like "c0 a2 b3 c3"
#eg. "c0 a2 b3 c3" --> -163.1541 which is x co-ordinate
    return decode_coordinate( j(wstr) );
    
def j( str ):#returns array
    #"c0 a2 b3 c3" ---> [127 162 33 33]
    array=str.split(" ");
    w=[];
    for x in array:
        w.append(i(x)); 
    return w;
def i( h ): # h is hex string  "ff"-->255
    return int(h,16);
def k( r ,l): # 176-->[176], 666-->[02, 154]
    hx=hex(r);
    hx=hx[2:];
    if(len(hx)%2==1):
        hx="0"+hx;
    c=[];
    for x in range(0, len(hx), 2):
        c.append(i(hx[x:x+2]));
    while len(c) < l:
        c.insert(0,0);
    return c;
def decode_coordinate( w ): #w must be array like [ 127 82 45 255 ]
    #[ 127 82 45 255 ] ---> -163.415 = x co-ordinate
    a=w[0];
    if( a < 192 ): # x must be positive
        y = (a - 64)*2 + 1; # 2^y <= x < 2^(y+2) y is odd
        w.pop(0);
        str = ""
        for element in w:
            h=hex(element)[2:];
            str+=h;
        z =  decodeFraction( str )
        if( z <= 0.5 ):
            x = z * pow(2, y+1) + pow(2,y);
        else:
            x=z * pow( 2, y+2 );
    else:
        y = (a - 192)*2 + 1; # 2^y <= x < 2^(y+2) y is odd
        w.pop(0);
        str = ""
        for element in w:
            h=hex(element)[2:];
            str+=h;
        z =  decodeFraction( str )
        if( z <= 0.5 ):
            x = z * pow(2, y+1) + pow(2,y);
        else:
            x=z * pow( 2, y+2 );
        x = -x;
    return x;
def decodeFraction( y ): #0.bbaa ----> 0.7856
    #y must be bbaa
    x = len(y);
    a = int(y,16);
    return a * (1/pow(16,x));
def encodeFraction( x ,d):  # to 3 places eg. 0.bba
    #now to d places.eg. ( 0.5,2) -->[8 0]
    a= x/(1/16);
    y = math.floor(a);
    if( d == 1 ):
        return [y];
    else:
        b = a % 1;
        z =encodeFraction( b, d-1 );
        z.insert(0,y);
        return y;
        
def encode_coordinate( x ):
    #162.444 ----> returns [ 127 45 25 255] as needed in wireshark
    #this is the first function i made.
    if( x == 0 ):
        return [0,0,0,0];
    if( x > 0 ):
       c1=64;
    else:
        c1=192;x=-x;
        
    y = math.floor( math.log2( x ) );
    bool = 0;
    if( y % 2 == 0 ):
        bool = 1;
        y-=1;
    x1= c1+(y-1)/2;
    if( bool == 0):
        y2=( x - pow( 2, y ))/(pow(2, y+1));
    else:
        y2= x/pow(2,y+2);
    temp =  y2/(1/(16*16));
    x2 = math.floor( temp );
    temp = temp - x2;
    temp = temp/(1/(16*16))
    x3 = math.floor(temp);
    temp = temp - x3;
    temp = temp/(1/(16*16));
    x4 = math.floor(temp);
    return [ (int)(x1),(int)(x2),(int)(x3),(int)(x4) ];