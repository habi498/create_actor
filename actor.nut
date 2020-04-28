function dR( data ) //data Received
{
	local i = data.find(" ");
	if( i != null )
	{
		local cmd = data.slice(0, i );
		local text = data.slice( i+1 );
		onBotCommand(cmd, text);
	}
}
function onBotCommand( cmd, text )
{
	if( cmd == "created" )
	{
		local i = text.find(" ");
		if( i != null )
		{
			local params=split(text," ");
			local name = params[0];
			local botID= params[1].tointeger();
			local skin = params[2].tointeger();
			local player = FindPlayer( name );
			if( player )
				player.Skin = skin
				print("Actor created\n"+"name:"+name+
				" botID:"+botID+" playerID: "+player.ID+
				" skin:"+skin);
		}
	}
}
function set_actor_skin(name, newSkin)
{
	local player = FindPlayer(name);
	if( player)
	{
		if(player.Name==name)
		{
			player.Skin=newSkin;
		}
		
	}
}
bs<-NewSocket("dR");//bot socket
bs.Connect("127.0.0.1",5555);
function execute(botCmd)
{
	bs.Send( botCmd );
	//name at least 4 letters
	//eg. "create_actor 5 medic  -662.383 749.163 11.1931 1.2"
	//angle -3.14 to 3.14
}