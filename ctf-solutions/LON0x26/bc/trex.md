Use a java decompiler like jd-gui to find some necessary data:

key: SunShellSunShell
iv: JoinSunCyberSec!
76, 105, 76, 57, 82, 109, 55, 70, 90, 86, 104, 68, 114, 87, 68, 100, 121, 51, 66, 98, 122, 90, 57, 81, 43, 79, 120, 73, 75, 78, 98, 105, 55, 109, 47, 69, 87, 77, 70, 99, 117, 118, 86, 61

Used the following CyberChef recipe (thanks GCHQ):

```
From_Decimal('Space',false)
ROT13(true,true,13)
From_Base64('A-Za-z0-9+/=',true)
AES_Decrypt({'option':'UTF8','string':'SunShellSunShell'},{'option':'UTF8','string':'JoinSunCyberSec!'},'CBC','Raw','Raw',{'option':'Hex','string':''})
```
