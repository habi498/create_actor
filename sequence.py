def encode_sequence_index(index): #1021-->fd 03 00
    #ie. [253 03 00]
    psn=hex(index)[2:];
    if(len(psn)%2==1):
        psn="0"+psn;
    seq_num=[];
    if(len(psn)==6):
        seq_num.append( int(psn[4:6],16) );
        seq_num.append( int(psn[2:4],16) );
        seq_num.append( int(psn[0:2],16) );
    elif(len(psn)==4):
        seq_num.append( int(psn[2:4],16) );
        seq_num.append( int(psn[0:2],16) );
        seq_num.append( 0 );
    elif(len(psn)==2):
        seq_num.append( int(psn[0:2],16) );
        seq_num.append( 0 );
        seq_num.append( 0 );
    return seq_num