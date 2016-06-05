function read_file(filename)
  local ifile = io.open(filename, "r")
  if (not ifile) then
    iup.Message("Error", "Can't open file: " .. filename)
    return nil
  end
  
  local str = ifile:read("*a")
  if (not str) then
    iup.Message("Error", "Fail when reading from file: " .. filename)
    return nil
  end
  
  ifile:close()
  return str
end

wndMsg1 = iup.multiline{size="80x60",expand="YES",value=""}
wndMsg = iup.multiline{size="80x60",expand="YES",value=""}

btn_image = iup.button{ title = "Button with image" }
function btn_image:action()
	debug.sethook(hookfunc,"l")
  dofile([[E:\MyProjects\OpenSource\Lua\IUP\iup-3.17_Examples1\iup\sample.lua]])
  --wndMsg1.value = read_file("iuplua.lua")
  --iup.Message("Hello World 1","Red button pressed")

  return iup.DEFAULT
end

isNext = false

btn_next = iup.button{ title = "Button Next" }
function btn_next:action()
  isNext = true

  return iup.DEFAULT
end

function hookfunc(event,line)
    local s = debug.getinfo(2).source --short_src
	if s==[[@E:\MyProjects\OpenSource\Lua\IUP\iup-3.17_Examples1\iup\sample.lua]] and line>=103 and line<=118 then
	    --CHook(s,line)
		--print(s .. line)
		wndMsg.value = tostring(s) .. line .. "\n" .. wndMsg.value
		printlocal("a")

		--[[
		b = iup.Alarm("IupAlarm Example", "Next" ,"Yes" ,"No" ,"Cancel")
  
		if b == 1 then 
		  --printlocal("a")
		elseif b == 2 then 
		  --printlocal("a")
		elseif b == 3 then 
		 iup.Message("Save file", "Operation canceled") 
		end
		--]]

		repeat
			iup.LoopStepWait()
			iup.LoopStep()
		until isNext
		isNext = false

	end
end
function printlocal(valname)
    
    --lua��û�����ݱ�������ñ�������Ϣ����������ֻ��ȡ��ջ�����б��ر�������Ϣ��
    --Ȼ��һһ�ȶԣ������Ƿ���Ҫ�鿴�ı���
    local i = 1
	wndMsg1.value = ""
    repeat
        local name,value = debug.getlocal(3,i) --��1���ǵ�ǰ��������2����c++�е�CHook,��3����hookfunc,��4���������Ҫ���ٵĺ���ջ
        if name == nil then
            --print("����������")
            return
        end
        if name ~= nil then
			wndMsg1.value = name ..":" ..tostring(value).. "\n" .. wndMsg1.value --.. value
            --return
        end
        i = i + 1    
    until false
end



dlg = iup.dialog
{
  iup.vbox
  {
    iup.hbox
    {
      iup.frame
      {                   
        iup.vbox
        {
          btn_image,
		  btn_next
        }
        ;title="IupButton"
      },
      iup.frame
      {                   
        iup.vbox
        {
          iup.toggle{title="Toggle Text", value="ON"},
          iup.toggle{title="",image=img1,impress=img2},
          iup.frame
          {                   
            iup.radio
            {
              iup.vbox
              {
               iup.toggle{title="Toggle Text"},
               iup.toggle{title="Toggle Text"}
              }
            }
            ;title="IupRadio"
          }
        }
        ;title="IupToggle"
      },
      iup.frame
      {                   
        iup.vbox
        {
          wndMsg1,
          wndMsg
        }
        ;title="IupText/IupMultiline"
      },
    }
    ;gap="5",alignment="ARIGHT",margin="5x5"
  }
  ;title="IupDialog Title", menu=mnu 
}

function dlg:close_cb()
  iup.ExitLoop()
  dlg:destroy()
  return iup.IGNORE
end

dlg:show()

--if (iup.MainLoopLevel()==0) then
  iup.MainLoop()
--end
