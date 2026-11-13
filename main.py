# SPDX-License-Identifier: MIT
# tiny-chess-01 entry: sunfish-2026 core, MTD-bi, node budget 40000 (deterministic)
import base64,lzma,struct,sys,os,json,urllib.request as u
from collections import namedtuple
from itertools import count
X=lzma.decompress(base64.b85decode(b';1Z1o-T?qO8-3#5+9nMoY`sHQCAjs1_KS7v|D|fP)Ns`HCridXM5Hqoc^@A`Huw@@3QZR6Cj~~-a*+UD8tUVazwZRwZNc^L)TzJN8O)75oihPzRO%~3B88Y;YrY447cl#Gns!jmd|9kyeVUiHA3J?>*KkdUOu;KD?W$c)TwD986)~Jcr5Z_Lm)soWTK=_OgJJrHd5+aO-fh8v$yxn>onQ<Zv2kndD1RKA9J<u^C2HFHc=kL8+Ncj}(q43=1{bd7>eL8N(<P+@CM9EgoR-3;!HMz18t(0CW`)9U`r7YDf+ztEWtTHd>(IafQf>mqtPI(g$+ibbsCM4*aqDi<<6aj_Zs?y`;`m>sKm!>=XMt7X>=8!3=~s~wh<iEe^T0y2cP(sT^c6<3*g;HAl<TZY`^-{2&$)PNcHD?xaWXeOI$SMnli(y7!7U$p&B6SYt&Kj3X8o>2udt1?noed+@0Wv68hEYB*}Vc$+JtO1r^!~{NqJH20M_{y<W4G*%>2ye|9lmf`mFi87b`;NG7zuv616UD08cyPJt+5L(S4eWbvSV3Z1MYT7A3h=KNITLToL1&Mb6Q8i-5g7ht1Zhh(7ySioMX12Tc+GoX;}IA7}_JfUe4U2^t}?xOpZLwnq``r6@{CKV4;m0%vA9bl34sKa`E_Puj2Csx0XVEEX)~(XfA(3`=lr#RiTBINDzOaLGC$@m|3z+84)~tz_1g=66{7bwDcgVQ|;uh&FKpwQdv?KQWe77*7Mbl6oUHfHd%kzVZ5(YjeSPX3;Av5ZPG&BoBLf4<~MYuXUARExOg^oSR!yl8a|Hcycmx^Z-4nI{#R)XWO>Mz)98{?{BI&$~~fU2IzppoY74b`A=|0&)WyNb^@NR-`P$X1u0^Kf7z~?t*O=ZvXXYMwo@LLW~89F{0n)ik?Sm_5rxvXtdj~Lx9N~ORIY_|2*sE{xIKYeH31?GMP>B2ZJtYZOeX%aqymvC#W};a6$L=a-f*6d;RRVw_G#-GmF}n;rBvdWeafpsYAR>ly*0btI@_rn-BDNj(6M!(6a6wAn%%eFQJyx4;O;K&j#i!gyNyZ;`aBRr-wmWD^^yv<Tz9{LOJ~5|px^LsPOyUer99q<5{Df9D}v}NQsK(FKgzH*LTJ@-B$}&s!ezFmVuJb|9`gW^S^lldyN0Z%v4wn@KqdqXH><I_%0(63s5eB>;~_S&MOh&Zwv{~1%{m&dtv9Hemg~)h^rO?&M*qh5nDMpjH-WafrELjLiYQ&hLv1PslCD_ge$DybRdWw74#&p=0C;fhB?2&f&$w?OlIo>3rnXpYqS!sQrxRSR>ke!6mz@G!GgPq|E6v6JV6(<{;K?`N5z#hChFU|0qtp#q?iEcf0wiLKyI;%Mc-q=^Vz0U`I{MTvT|7Hi5jOzhdGBB{y0H#A?rX;2@9kB1X@W&_ECyMxx;}qcmss0VTDnchf`xfro@0@Gq1<MAu)vkzBzTSbgjpZ)y(VPp^ACJs18So_+^f62BCQ2!vyx)1o4hJhZOC%Vy`T}Yjo~pKkjSy5iz3$pws%8Me==xVpm}tSmJBCNQ-zmKNVb<}-aaW+6EV>d$u)n9wpq(91aRh&B`+n|R+n691>{m!^TShZv60MLh{Y1M4h^6Of0DG(@%X-RfWw<;fd8+`O$!_l=`gOYhzf@2u<5AMfE%(ao07bpXtz?En`l$%Gnupo`kBkUrUlyDEFYBkgP)Db%x%aLZMjEkeOxHc#OpEgPtaamx-+E}W;hjhDPX7MK-!hs49GfxEsKbZF4tS-3K4Am2BX65hQG=97?WIJ&>Y&=ni@GkdX`rzbGe9&lKP(=t<?+c`ejv|HCMeSSXd2_V`5-FvX!@#`t>&f_mtR?P=9N3H^BvyWjLGNH_QD0*d1B!=f@ZHtr-Xe!WbeRL@+e84PD!;jJX#zsVC8}Y7HKEyJ%R`S)U1;Ff<acXQ_9&e+$G;x#0#!hw?MvCb8BRu4e!K&}pl1_~w;)Z>Qad9X}v{dOp0eE|`J^&AxiL^h;H=%wd2IQ}#R40`unkF%3Q6!m__lp4Serm2O|%_XrGKO^V3&>N0<D9{8)?FCijYv>k`;0d;&w%09^SD<59`((v0c)lnE+cM9NH=oBXhyPr)qFn}H|L-157dH@m6&S>i+ZaPPXY(r9}$V7x+0TapJl#H_oZ>Q2VgEx!F&^)oYsr6*vd@~-OKf&?rpKKhnBg=?>se_dXD*lwd#hm+OUo#zj@pG?#MfX~n?(pw+(FL;FigIRh_vogpk#~mhY{#;C>|NmYBgWD=B5D@C)x4Zx;4%&C(#@4SBSXHj&U&c#PAv<f)@}F$)@1E1l$oqOa#y!|0<rNHH3kK@wtctPTk{G6%}So!e7us`TD%BqPYApb%<@OGiKS{4$qYLuXl6(uJUh{Z?~g=?MmQ(Kn}eGvtg6UgB<*HQg}ske{JU*wE^d$nOfIZWFyaJB&t-fFE=8lWjH&mVF=dZj4Y+Dluyx9p;SrcUpiyrfLAy{_k~~>HKTUwwI^_UCI#h})w7U*B(^&oBrXy`|fy>7f8E&ABpE;TTCB)SJ!=KP3n*a'),format=lzma.FORMAT_RAW,filters=[{'id':lzma.FILTER_LZMA2,'preset':9,'pb':0,'lc':1,'lp':0}])
v=struct.unpack('<384b',X[-384:])
G={'pst':{k:v[i*64:(i+1)*64] for i,k in enumerate('PNBRQK')},'namedtuple':namedtuple,'count':count}
exec(compile(X[:-384].decode(),'sf','exec'),G)
P=G['Position']
class N(G['Searcher']):
 BUD=40000
 def bound(self,*a,**k):
  if self.nodes>N.BUD:raise G['Stop']
  return super().bound(*a,**k)
q=lambda i:chr((i-91)%10+97)+str(1-(i-91)//10)
def f2p(f):
 p=f.split();B='         \n'
 e=B+B+''.join(' '+''.join('.'*int(c) if c.isdigit() else c for c in r)+'\n' for r in p[0].split('/'))
 o=P(e+B+B,0,('Q' in p[2],'K' in p[2]),('k' in p[2],'q' in p[2]),0 if p[3]=='-'else 91+ord(p[3][0])-97-10*(int(p[3][1])-1),0)
 return o.rt() if p[1]=='b' else o
# moves: queen promotions only (size cap); engine plays legal queen promos
def ch(f,L):
 s=N();b=None
 try:
  for r in s.search([f2p(f)]):
   b=r[3] or b
   if s.nodes>N.BUD:break
 except G['Stop']:pass
 if b is None:return L[0]
 i,j,p=b
 t=q(119-i)+q(119-j)+p.lower()
 return t if t in L else next((x for x in L if x[:4]==t[:4]),L[0])
E=os.environ['MAKEFUN_ENV_URL']
post=lambda a,b:json.load(u.urlopen(u.Request(E+a,data=json.dumps(b).encode(),headers={'content-type':'application/json'})))
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':ch(g['fen'],g['legal_moves'])})
