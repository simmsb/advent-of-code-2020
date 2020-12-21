from collections import defaultdict
from typing import DefaultDict
import z3


def parse_food(inp):
    ing, contains = inp.split("(contains ")
    ing = ing.strip().split()
    contains = contains.strip(" )").split(", ")

    return ing, contains

def bothparts(foods):
    s = z3.Solver()

    all_ingredients = list(set(i for ingrs, _ in foods for i in ingrs))
    ingredients_idxs = {ing: i for i, ing in enumerate(all_ingredients)}
    all_allergens = list(set(i for _, allergens in foods for i in allergens))
    allergens_idxs = {alg: i for i, alg in enumerate(all_allergens)}

    idxs = [z3.Int(f"idx_{i}") for i in range(len(all_allergens))]

    for i in idxs:
        s.add(i >= 0, i < len(all_ingredients))

    s.add(z3.Distinct(idxs))

    for ingr, allergens in foods:
        for allergen in allergens:
            idx_var = idxs[allergens_idxs[allergen]]
            s.add(z3.Or(*[idx_var == ingredients_idxs[ing] for ing in ingr]))


    assert s.check() == z3.sat, "fuck"

    m = s.model()

    assignments = [(all_allergens[i], all_ingredients[m[idx].as_long()]) for i, idx in enumerate(idxs)]


    okay_ingrs = set(all_ingredients) - {ing for _, ing in assignments}

    total = 0

    for ingrs, _ in foods:
        for okay_ingr in okay_ingrs:
            if okay_ingr in ingrs:
                total += 1

    assignments = {ing: alg for alg, ing in assignments}

    dangers = ",".join(sorted(assignments.keys(), key=lambda ing: assignments[ing]))

    return total, dangers


inp_o = """
qqskn vqm rxhxs xhzr lpxb plc sksqn hcfjt xjqd vgnf shln ccvnlbp btnmj lvntbhnk kl pdvqq pcbls jnqcd xbvm fdbd thpt thjblh dhcbcm kltmhv zxql hnfpxh kcvsl bkbpjf stkqcn lkkb bnj psxb pxmrdg fhcms cdl xkbzbsf rfhz pvkmx qjqb jzfxc glrps kqxmv lvdhspf bsqxjk xdtt cjxv jhzllk bhbhz rfhrps zgsm lccs mnz grnm bgvx xkjng pkzjv vmskhmg dssdlb fnnkfq gbmldv rplg qmgbz nzbbzd kgzjj gq nhclz (contains dairy)
nfngm ccvnlbp fnnkfq dnz vrjmh tldgnn lbgc cjxv kbcc qqskn zgxrt zks xkvcq qjqb hsjfvb klpvh sksqn xjqd thjblh rlcjkc rplg qmjjb fzqds hdmx fzksgr hcfjt pxmrdg btnmj skg llszv qkgj hngv xxvg bjtftkjv zfxsbphz tbvpmf tcm jnqcd kshmt vpfjnk qrrz vfcq tknpg pkj mnrks kqxmv gphf (contains nuts, soy, peanuts)
qxxtt pvtmb tkbl tldgnn xbvm lxzs lflgp kpnmg pkzjv qjqb nbcdr qqskn glrps jvzjzb jzfxc xhr thpt dlhj cdl kl bqrkh cmkj hnln dgdr mtcgr jnqcd nfngm cjxv hmg gbmldv nskx jrjshr qmgbz ccvnlbp vpdk xkvcq qzftq bzzl mcdgk pvkmx rplg nhclz fvmql sfvhg zxql hngv fhnxhq srhqgm rgv zks tbvpmf xhzr kshmt lxfqzvk hsbvtfvf pcbls bnj lpxb hmvcc rfhrps rjppgdl tnhfjhj mmh gphf bjtftkjv fszzx hdmx lzhqznp bxqxs tcm bkbpjf klpvh pdvqq (contains fish, nuts, eggs)
tdssg nxnbq tsglv tkxn mbpfmjcl dskp gq srhqgm xkjng tnhfjhj jnqcd dgdr kgzjj rplg hdmx cjxv mmh pxmrdg fzqds rfhrps qqskn sxqvc qmvblt bltcxf xhzr vfcq sdjnd txhgkp bkbpjf grnm fhcms skg qjqb jhzllk fvmql xhr ccrd rxhxs xdtt dlhj rjppgdl dssdlb vrjmh bgvrr ccvnlbp grmzrf fpxqm fsjk hldjv srzq sksqn qmgbz zcf xjhjtt thpt qkgj fdrl hmg tcm llszv xhlxtg cdl dnz (contains nuts, eggs)
bxqxs llszv xxvg ttvkj zgxrt lpxb fdrl kljktfm cjxv lccs hmg zbpmtj ccvnlbp xkvcq kgzjj fskxb qqskn hsbvtfvf hnfpxh tnhfjhj hmvcc cmkj hcpdd vrjmh xhzr fdbd vpdk vgnf xjqd pkzjv thpt rfhz bnnxlfn pvtmb cqd plc mnrks bgvx tcm jnqcd nbcdr grnm hsjfvb jzfxc bqrkh rlsvj rvmqk pdvqq bnj vtqm rjppgdl jjbkfh bltcxf fkchxn btnmj lbgc gvxnm (contains fish)
jgz svrs sfvhg xkjng cqd mcdgk kljktfm mnz xjqd tcm xhzr lxzs xbpl dssdlb nbcdr rgv fdrl jzfxc bjtftkjv lkkb rvmqk bqrkh pdvqq djkfgqv txhgkp kbcc lfsf srhqgm rfhrps gphf hldjv xhlxtg qrrz cgmdhkb dlhj qqskn kgzjj cmkj hppdqbr tknpg jjbkfh lzhqznp jrjshr jnqcd qknvdk hmg tkbl hdmx zgxrt zks bzzl xbvm lflgp gq rjppgdl bkbpjf glrps fnnkfq xdtt srzq rplg qjqb ccrd bxqxs hngv dskp cjxv (contains dairy)
qxxtt xxvg klpvh fdbd jnqcd cjxv tnhfjhj dhcbcm qjqb hppdqbr vmskhmg tknpg rfhz hcfjt sxqvc kljktfm bhbhz hcpdd ccrd vzfvp jzhs xjqd ccvnlbp txhgkp mxkfgxj tsglv mmh rvjpn vhdm qmgbz rvmqk vxsrx xhr zxql lflgp bsqxjk tbvpmf glrps nskx gq tcm qqskn vrjmh jhzllk hrgzhpk qmjjb tkbl xkjng sdjnd srhqgm vtqm kshmt frprgrh pvtmb bnnxlfn lkkb jrjshr xbvm zcf (contains peanuts, eggs, soy)
xhr bnnxlfn slrxkmd rlcjkc pvtmb srzq zcf lbgc zgsm hnfpxh vxsrx txhgkp bltcxf xjqd jjbkfh hsbvtfvf llszv mtcgr cjxv dnz pkj vtqm xhzr mmh bhbhz nskx lzhqznp ttvkj cdl pdvqq fdrl hppdqbr hcfjt xdgmppd vpfjnk pkzjv rfhz qzftq zkdd gvkkqs xkvcq thpt fzg qjqb gvxnm qqskn lccs qxxtt psxb mcdgk pvkmx ccvnlbp kcvsl xkjng jhzllk xbpl xkbzbsf dgdr qmgbz fhcms klpvh vqm fnnkfq rgv dssdlb gphf kshmt btnmj bxqxs nbcdr jnqcd fzksgr qmvblt jrjshr lxzs kbcc bzzl vpdk (contains soy, eggs)
mnrks bqdtq kqxmv fzg qzftq dskp xhr zgxrt kljktfm pvkmx jjbkfh lxfqzvk xkbzbsf vqm rplg vpfjnk xhzr cfklrp rvmqk lvntbhnk kl cqd xbvm sdjnd hsbvtfvf txhgkp xdgmppd thjblh kltmhv hsjfvb svrs bqrkh pkj rfhz sxqvc bzzl mmh nhclz tcm vrjmh tldgnn qkgj xbpl nxnbq xjqd kgzjj lpxb cjxv cgmdhkb xkjng hcpdd rlcjkc hppdqbr qqskn klpvh fkchxn rxhxs qmjjb jnqcd pcbls lvdhspf fhnxhq bxqxs lccs sksqn vhdm zbpmtj qknvdk hnln grmzrf gvxnm vmskhmg nzbbzd ccvnlbp kshmt xhlxtg fzksgr vxsrx jgz (contains soy)
zks dnz dlhj rfhrps vpfjnk qqskn tkxn vpdk qmjjb hcfjt sxqvc dgdr zfxsbphz tcm bxqxs dssdlb lvntbhnk zxql hnln hsjfvb cjxv fpxqm ccvnlbp sfvhg xhzr plc grnm vzfvp hcpdd fvmql qxxtt dhcbcm fzg xjqd qmgbz thpt lzhqznp nxnbq pkzjv mnrks tnhfjhj gphf mmh fdbd jnqcd xhr (contains nuts, fish)
kpnmg hnfpxh vmskhmg hnln xbpl hmg ttvkj dgdr thpt nbcdr pdvqq llszv kqxmv tcm tnhfjhj hcpdd hdmx qqskn rjppgdl jzhs thjblh srzq fszzx rplg txhgkp bltcxf kljktfm xkjng xhzr mtcgr djkfgqv zcf zfxsbphz bqdtq lkkb vqm kl lxhrj bhbhz xdtt kcvsl xjqd rgv lpxb klpvh vpfjnk kltmhv nxnbq pvtmb fhcms tvsdc zgsm dskp vfcq fzg fnnkfq qjqb bjtftkjv xjhjtt zgxrt stkqcn mxkfgxj lvdhspf ccvnlbp tkbl vrjmh qrrz gbmldv cjxv bxqxs bkbpjf lxzs lfsf hrgzhpk zks hngv (contains soy)
mbpfmjcl kshmt qjqb zkdd srhqgm zks fzg tvsdc bnj hdmx glrps gvxnm hmvcc jjbkfh pkj rvmqk qmjjb jnqcd xdgmppd lfsf lvntbhnk cjxv qmgbz dssdlb hmg tknpg qqskn fdrl tdssg jvzjzb thjblh xhzr fkchxn tbvpmf lxhrj nskx nbcdr cqd vzfvp cdl lflgp zfxsbphz lvdhspf djkfgqv zcf hsjfvb jhzllk hldjv ccrd kpnmg vfcq mtcgr qmvblt sksqn fhcms lzhqznp jzhs bqrkh dhcbcm vhdm qrrz kcvsl xbpl hnln xxvg xjhjtt kl rxhxs frprgrh qxxtt llszv gbmldv gphf ccvnlbp vpfjnk xjqd bhjn bgvx lccs bxqxs kgzjj vpdk fhnxhq (contains soy)
vqm pcbls qkgj hngv qjqb bqrkh rjppgdl dhcbcm zbpmtj mmh jnqcd lzhqznp zfxsbphz xkbzbsf jhzllk txhgkp rfhrps pvkmx kpnmg ccvnlbp bqdtq hppdqbr vpfjnk bgvrr tcm rvjpn mxkfgxj fvmql bhjn rplg lxfqzvk qqskn tdssg sdjnd xhzr nskx zcf xbvm pvtmb mcdgk xhr mbpfmjcl cmkj zks qmjjb btnmj hnfpxh fzksgr bxqxs kcvsl xjqd bltcxf bgvx tldgnn dnz hsbvtfvf lflgp tbvpmf (contains fish)
qmvblt tldgnn pcbls bsqxjk vqm lzhqznp klpvh vpfjnk xkbzbsf jzfxc pkj rjppgdl nfngm nhclz sksqn kltmhv zkdd kcvsl hcpdd fhnxhq mcdgk zbpmtj lvdhspf rplg zxql bnnxlfn xhlxtg hmg ttvkj dlhj crmn qmjjb dssdlb cjxv xhr slrxkmd vpdk tknpg xbpl cgmdhkb sxqvc bhbhz xdtt hsjfvb pkzjv fzg fszzx mtcgr qqskn ccvnlbp zgxrt rfhrps jrjshr stkqcn xkvcq tcm tvsdc xjqd mxkfgxj bzzl thjblh xbvm glrps jnqcd bgvx qzftq xkjng rfhz hcfjt srhqgm fkchxn vrjmh rvmqk zfxsbphz tkxn vfcq vzfvp hppdqbr tkbl bkbpjf kshmt pvtmb pxmrdg hsbvtfvf vhdm zks xhzr (contains dairy, sesame)
mtcgr lzhqznp xjqd vqm qmvblt xhzr xbvm ccvnlbp tknpg bnnxlfn sfvhg kljktfm lvdhspf hnln vrclpzm xxvg vrcrg pkj tcm zcf svrs vfcq nfngm pvkmx cjxv dssdlb klpvh cgmdhkb vmskhmg bjtftkjv ccrd nskx fsjk qqskn gvkkqs qxxtt fszzx srzq tsglv xkbzbsf kqxmv qjqb vgnf fpxqm mmh bqrkh bqdtq zfxsbphz fhnxhq fkchxn vxsrx jjbkfh cfklrp mnz (contains fish, eggs, dairy)
ccvnlbp zgsm bltcxf jnqcd grmzrf hsbvtfvf kqxmv qkgj tcm fzksgr vpfjnk mxkfgxj qqskn qjqb zxql tldgnn vgnf lpxb grnm thjblh psxb cfklrp lfsf xhr lxhrj xkvcq mtcgr tkbl rvmqk slrxkmd bnj xjqd fsjk qmjjb zbpmtj pcbls kgzjj pvtmb lbgc kshmt vtqm hnln xxvg fhcms fszzx jzfxc hnfpxh bgvx bqdtq bgvrr rfhrps xkjng hmvcc plc cmkj bzzl xbpl qknvdk ttvkj tdssg xhlxtg klpvh hrgzhpk xkbzbsf glrps srzq cjxv hcpdd pkzjv rfhz (contains nuts, dairy)
zbpmtj xjqd nbcdr fkchxn hppdqbr qjqb hldjv rgv hmvcc rfhz bkbpjf vrcrg hsbvtfvf qmjjb srzq xhzr stkqcn zks mnz ccvnlbp cjxv bltcxf zxql qqskn tcm klpvh lzhqznp pvtmb lflgp rvjpn rplg mmh mtcgr (contains soy)
dhcbcm dlhj zfxsbphz xjqd jjbkfh lbgc tcm bnnxlfn qmvblt nfngm hcpdd pkj lxzs psxb rlcjkc hmg kltmhv gvxnm fhcms qjqb fzg bzzl lfsf vpdk vpfjnk qxxtt ccvnlbp srhqgm kbcc jnqcd cgmdhkb hngv hrgzhpk nxnbq vqm xhzr pdvqq cjxv gq rvmqk rfhrps tkbl txhgkp kgzjj vrclpzm (contains shellfish)
xhr jnqcd vfcq hdmx hcpdd bqrkh xjhjtt vtqm dskp fszzx rplg skg dhcbcm qmgbz rfhrps pkzjv jgz pkj vpfjnk slrxkmd rgv kltmhv xxvg xhlxtg fnnkfq kqxmv hmvcc lzhqznp gq tbvpmf cdl kshmt rvmqk xhzr qrrz mnz hsbvtfvf fhcms xkvcq dgdr nbcdr fsjk fdrl thjblh cjxv gvxnm vpdk xbpl kbcc txhgkp sxqvc qqskn jhzllk djkfgqv gbmldv qxxtt pdvqq lflgp ccvnlbp qkgj gphf xdgmppd shln psxb tsglv rlcjkc lccs vxsrx jzfxc qjqb hcfjt pxmrdg lbgc vrjmh tcm jjbkfh mtcgr qzftq qknvdk bgvx (contains soy, peanuts, shellfish)
qjqb lkkb lvdhspf zbpmtj sxqvc frprgrh lbgc bltcxf qknvdk kqxmv svrs bjtftkjv pkj zgsm fdrl kbcc rjppgdl hrgzhpk nbcdr vpdk fsjk tcm vrclpzm plc nfngm kshmt xhlxtg dssdlb qzftq pdvqq lxhrj kltmhv sfvhg nzbbzd tkbl ccvnlbp xkbzbsf pcbls skg cjxv tldgnn xjqd zxql qqskn xhzr dgdr nhclz hsjfvb hmvcc fdbd bnj rxhxs (contains soy, shellfish, peanuts)
crmn zbpmtj vrcrg rvjpn jvzjzb hppdqbr slrxkmd hrgzhpk lvdhspf rfhrps cfklrp kpnmg jgz gvkkqs mxkfgxj fvmql btnmj mmh xhr qknvdk hnfpxh nskx tldgnn xjqd jnqcd kcvsl qqskn rxhxs dhcbcm nxnbq qmgbz bsqxjk ccvnlbp lxzs lkkb srhqgm tvsdc xdgmppd qxxtt pkj rlcjkc hngv gvxnm tkbl fdbd nhclz hcpdd zxql jjbkfh thjblh lccs zfxsbphz lvntbhnk qzftq bhjn tknpg fsjk bqdtq gq hmg hsjfvb gbmldv tcm mnz hdmx rlsvj qjqb qmvblt tkxn bltcxf qkgj rvmqk cgmdhkb lxhrj xhzr kqxmv grnm xhlxtg plc pvkmx (contains nuts)
sfvhg xhzr cmkj tldgnn nskx dssdlb nzbbzd dhcbcm zks cgmdhkb rfhz glrps rgv hrgzhpk hmvcc zxql qzftq srzq vgnf gq cjxv bhjn qjqb tknpg xxvg fzg xkjng psxb hcfjt bqrkh crmn vqm rfhrps xkbzbsf hcpdd xhr sksqn tcm lkkb xjqd pvtmb qknvdk qqskn rjppgdl rvjpn zgsm djkfgqv jnqcd bltcxf vhdm grmzrf slrxkmd (contains peanuts, nuts, shellfish)
rvmqk hppdqbr vzfvp ccvnlbp tkbl hldjv fhcms xhlxtg grnm vxsrx qknvdk mxkfgxj zgxrt pdvqq slrxkmd dgdr zgsm hdmx vrclpzm xbpl lxzs cjxv xdtt kltmhv rfhrps zxql pcbls fszzx qxxtt thpt lfsf qjqb mcdgk kpnmg lpxb fskxb xkjng bgvx lflgp hmg cfklrp mnz zkdd bzzl vrjmh bnj grmzrf tcm srhqgm btnmj hcfjt cmkj hsjfvb xkvcq tbvpmf tvsdc crmn lzhqznp srzq kcvsl kqxmv rvjpn dlhj dskp bkbpjf rxhxs zfxsbphz tknpg fvmql fpxqm qqskn ccrd xhzr xjqd hsbvtfvf kbcc klpvh hngv dnz cgmdhkb (contains peanuts, eggs)
jnqcd lxhrj qjqb gbmldv xbpl kshmt djkfgqv mcdgk rlcjkc rplg jhzllk lvntbhnk fkchxn xjqd tkxn grnm cjxv vrclpzm xhzr llszv ccrd lkkb lbgc bxqxs vmskhmg fhcms vxsrx qqskn ccvnlbp vtqm cgmdhkb bnj lxzs lpxb gvkkqs tnhfjhj fszzx pxmrdg tvsdc (contains dairy)
lflgp bsqxjk btnmj tcm xxvg qmgbz ccvnlbp frprgrh glrps tdssg jnqcd xjqd lvntbhnk mcdgk qjqb cjxv zks plc mnz bnj fskxb vrcrg jgz nhclz grnm gbmldv stkqcn qrrz rlsvj mmh xdgmppd tkbl gq cgmdhkb kljktfm bhbhz vpfjnk rvmqk tknpg qknvdk tkxn tvsdc mbpfmjcl qqskn crmn rfhz srhqgm vqm gphf cqd pkzjv qkgj tldgnn fzqds bqrkh vtqm sfvhg hcfjt nbcdr hppdqbr fsjk bqdtq ccrd (contains soy, nuts, fish)
cjxv kljktfm lfsf fszzx lzhqznp pkzjv dskp stkqcn xdtt lkkb xjqd qqskn dhcbcm pcbls dgdr kltmhv bqdtq gvkkqs kbcc vmskhmg mbpfmjcl fzqds tsglv hnln qjqb gphf llszv btnmj pvtmb psxb nfngm qmvblt hngv tknpg dnz frprgrh xhzr pdvqq tcm nxnbq sdjnd vrcrg qmjjb lccs plc cmkj txhgkp tbvpmf hldjv rlcjkc jgz nhclz xjhjtt fsjk kpnmg srhqgm sxqvc xkjng vrclpzm mnz rlsvj tkxn ccvnlbp (contains sesame, peanuts, dairy)
jjbkfh hmvcc qzftq tbvpmf qqskn grnm nskx jzhs dhcbcm bqdtq cqd cfklrp qmjjb rxhxs tvsdc cjxv zks kgzjj vrjmh grmzrf sxqvc fzg lkkb xjqd zkdd mbpfmjcl pvtmb srzq hcfjt bsqxjk nxnbq hnfpxh jgz xdgmppd nhclz pxmrdg fvmql djkfgqv jvzjzb fzksgr qjqb rlsvj zfxsbphz rlcjkc bltcxf ccvnlbp tcm kpnmg rvjpn kshmt jnqcd qmgbz mnrks txhgkp mxkfgxj lbgc tdssg qxxtt rgv jrjshr bkbpjf vqm qkgj sdjnd fdrl klpvh (contains nuts)
hnln bgvrr bqrkh dssdlb lvntbhnk hrgzhpk lvdhspf qqskn vxsrx lxfqzvk llszv crmn fzg tnhfjhj nfngm bxqxs hsjfvb mxkfgxj shln lbgc qmjjb fkchxn vpdk rvmqk xhlxtg qkgj hmg glrps fpxqm grnm thjblh xkvcq jnqcd hcpdd fhcms rlsvj rfhrps gvxnm rgv xdgmppd vrclpzm ccvnlbp xjqd xhr hsbvtfvf nskx sdjnd hngv lkkb cfklrp tkxn lfsf nxnbq hcfjt tvsdc bzzl nhclz zkdd ttvkj vqm jzfxc fhnxhq gphf sksqn fszzx svrs zbpmtj hnfpxh lflgp qmvblt rvjpn qjqb dskp rfhz cjxv xbvm tcm kbcc lxhrj (contains eggs)
jrjshr dhcbcm fpxqm lbgc slrxkmd vrclpzm fsjk fkchxn qjqb hmg hnln tbvpmf xxvg xhzr xkbzbsf bsqxjk kcvsl qmjjb xjqd zxql jgz srzq sfvhg bnnxlfn lkkb qrrz hcpdd mcdgk tkbl nxnbq plc vpfjnk svrs dgdr tcm kbcc nfngm stkqcn grmzrf pvkmx pkzjv xdgmppd mxkfgxj lvntbhnk qqskn cgmdhkb rfhz ccvnlbp gphf rxhxs vrcrg lvdhspf gq bkbpjf bltcxf qmgbz mnrks lxhrj qknvdk xkjng dlhj cfklrp vxsrx gvxnm cqd bhjn vgnf xhr fhcms cmkj bqrkh kshmt shln cjxv bgvx vfcq vpdk bnj fdrl hsbvtfvf btnmj rvmqk fzg vzfvp djkfgqv fszzx xhlxtg frprgrh (contains shellfish)
vrjmh pcbls lbgc vgnf kqxmv bjtftkjv kljktfm tknpg jnqcd hnln rvmqk rlcjkc fzqds fsjk xhr tcm hsjfvb vtqm ccvnlbp tkbl fpxqm dhcbcm kl dnz hcfjt cjxv mbpfmjcl nskx svrs bkbpjf rfhrps tsglv qqskn txhgkp fzksgr nbcdr zkdd btnmj cfklrp nfngm bgvx xbpl thpt qrrz gbmldv qmvblt lpxb vhdm hsbvtfvf lvdhspf qjqb pvkmx jhzllk rgv tvsdc jzfxc tbvpmf kshmt xxvg rxhxs xhzr jgz bqdtq gvxnm zks lccs hcpdd glrps (contains dairy)
nbcdr kl mbpfmjcl bzzl jhzllk hrgzhpk kljktfm xhzr srzq vmskhmg fzqds ccvnlbp lflgp lzhqznp vfcq hmg xbpl stkqcn lpxb zgsm vpfjnk qjqb vhdm vqm dhcbcm tcm vrjmh fdrl dnz zfxsbphz pxmrdg sfvhg nzbbzd tnhfjhj dssdlb svrs rvjpn zkdd jzfxc sdjnd rgv lxzs mcdgk mtcgr jrjshr fkchxn fvmql rlsvj tkxn xbvm jvzjzb ttvkj gvkkqs bhbhz jnqcd hppdqbr qkgj rfhrps skg pkj qqskn fszzx pkzjv fsjk lxhrj vzfvp pvkmx qmgbz xjqd (contains dairy, fish)
fskxb sxqvc gq lfsf rvjpn xbvm zxql bltcxf mcdgk skg slrxkmd xhr xjqd bgvrr bqdtq fhcms lkkb psxb rfhz fhnxhq tcm lbgc xdgmppd fzg nzbbzd nskx jzfxc zkdd kbcc dskp mxkfgxj qjqb xhzr kqxmv kljktfm hcfjt hppdqbr sdjnd hldjv bkbpjf jzhs lccs ccvnlbp tkbl btnmj xhlxtg tsglv fdbd sksqn hmvcc stkqcn xjhjtt bzzl pvtmb zks hmg jnqcd hnln fzqds jgz qqskn rfhrps xkjng thpt lflgp srzq mmh cmkj mbpfmjcl cqd dgdr zcf xkvcq tvsdc bnj lxzs gvxnm (contains fish, nuts)
tbvpmf svrs qjqb fnnkfq dlhj tkbl lkkb jnqcd hsjfvb hrgzhpk xjqd nbcdr kgzjj pcbls stkqcn lxhrj mbpfmjcl fhnxhq tknpg plc cdl nxnbq rjppgdl lfsf tcm tldgnn bqrkh gphf slrxkmd vzfvp bhjn kshmt rfhrps zcf fszzx kl qmvblt grnm bgvx ccvnlbp gvxnm qqskn jgz jzfxc kpnmg lvntbhnk hldjv dssdlb jvzjzb kltmhv sfvhg gq ccrd fsjk lpxb lvdhspf vgnf sxqvc mtcgr xhlxtg bgvrr gbmldv xhzr qxxtt (contains sesame)
lbgc vpfjnk xbvm psxb jvzjzb xdtt qqskn rxhxs bnj qrrz svrs vrjmh jhzllk cjxv jnqcd tcm mtcgr fnnkfq thpt xhr jjbkfh kshmt ccvnlbp pxmrdg glrps tkxn mmh nhclz xjqd xjhjtt vrcrg xhzr hsbvtfvf qmvblt djkfgqv bhbhz nxnbq rlcjkc bsqxjk dgdr vpdk (contains eggs, fish, dairy)
pxmrdg tcm jjbkfh bxqxs rvjpn mxkfgxj qknvdk tkxn lxzs rxhxs hppdqbr vrcrg mcdgk hmg xbvm lpxb bhjn bjtftkjv vzfvp rgv cfklrp bltcxf kljktfm tdssg qjqb lkkb cdl sdjnd klpvh qmjjb rplg stkqcn bgvrr tvsdc jzfxc kshmt kcvsl fdrl lzhqznp xjqd zxql vrclpzm pkj nhclz kltmhv zgsm zcf vrjmh xhzr psxb tnhfjhj jnqcd vxsrx bgvx cgmdhkb sxqvc fskxb fhcms lxfqzvk dgdr llszv jgz xjhjtt qqskn qxxtt hcpdd grnm bnj vgnf bqrkh hdmx ccvnlbp (contains fish, eggs)
rplg qqskn lxfqzvk hnln thjblh sdjnd pvkmx vpdk cdl txhgkp ccvnlbp zgsm bxqxs tkxn cjxv zks btnmj ttvkj rlsvj sfvhg mtcgr shln kshmt qmjjb mnz tcm lflgp xdtt djkfgqv pdvqq vpfjnk jrjshr kgzjj nbcdr rvjpn rxhxs skg hcpdd crmn grnm gvxnm tnhfjhj kljktfm dnz jnqcd cgmdhkb kltmhv rvmqk klpvh bsqxjk zgxrt jjbkfh fzqds xhzr qrrz xjqd hppdqbr fsjk hsjfvb kbcc cqd svrs fzg jvzjzb zxql lkkb fhcms vrcrg mnrks hdmx kcvsl jzhs (contains nuts, soy)
kltmhv cdl vpfjnk lpxb kqxmv nfngm xjqd pxmrdg fzg pvkmx slrxkmd lvdhspf jnqcd vrjmh sfvhg qknvdk gq fkchxn bqdtq lvntbhnk lfsf bjtftkjv ttvkj ccvnlbp tknpg hmg bgvx fdrl zks kgzjj mmh mcdgk xbpl zgxrt nhclz rlcjkc kshmt xkbzbsf qjqb hngv hsbvtfvf vfcq kl tcm kpnmg dnz rvmqk tvsdc bkbpjf crmn cfklrp btnmj ccrd vrclpzm dskp tdssg klpvh xjhjtt qkgj grnm tbvpmf shln xhlxtg cjxv fdbd gbmldv hrgzhpk qqskn dgdr (contains peanuts, soy, sesame)
qmjjb slrxkmd qjqb xdgmppd vfcq vrclpzm hsbvtfvf vxsrx grmzrf kljktfm xdtt tcm bzzl vqm mtcgr rgv nbcdr lkkb xhr thjblh btnmj ccvnlbp svrs gbmldv qknvdk jzhs dssdlb srzq qmgbz zxql bltcxf glrps bnnxlfn hnfpxh bhbhz cfklrp lfsf rplg fzksgr rfhrps hmg gvkkqs sksqn nhclz rlcjkc mcdgk pcbls jvzjzb xhzr xhlxtg pkj lzhqznp bsqxjk hngv jnqcd bgvx vtqm tnhfjhj fdbd hmvcc xkvcq xbvm zfxsbphz vrcrg jrjshr bqrkh xjqd qqskn crmn rvmqk fvmql rfhz tkxn hsjfvb pvtmb zgsm fhnxhq vgnf bgvrr jhzllk bnj (contains fish, sesame, nuts)
""".strip().splitlines()

inp = [parse_food(x) for x in inp_o]


ex_inp_o = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""".strip().splitlines()

ex_inp = [parse_food(x) for x in ex_inp_o]
