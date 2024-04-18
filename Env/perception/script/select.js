function selectChild(child, verbose = false) {

    let par = child.parentElement;
    let par_select = 'body';
    if (par.tagName !== 'BODY') {
        par_select = selectChild(par, verbose);
        if (verbose) {
            console.log("par_select:", par_select);
        }
        if (par_select === "") {
            return "";
        }
    }
    let iname = child.tagName;
    // let icls = child.getAttribute('class') ? child.getAttribute('class').split(/\s+/).filter(Boolean) : [];



    // let fea = iname + icls.map(cls => '.' + cls).join('');
    let fea = iname;
    fea = fea.replace(/\.{2,}/g, '.')
    let res = par_select + ' > ' + fea
    let idd = child.getAttribute('id');
    if (idd) {
        res = '#' + idd
    }
    let testlist = [];
    try {
        testlist = document.querySelectorAll(res);
    }
    catch (error) {
        idd = "";
        res = par_select + ' > ' + iname;
        testlist = document.querySelectorAll(res);
    }
    if (verbose) {
        console.log(res);
        console.log(testlist.length);
    }
    if (testlist.length === 0) {
        return '';
    } else if (testlist.length > 1) {
        res = par_select + '>' + iname
        if (idd) {
            res = '#' + idd
        }
        let testlist2 = document.querySelectorAll(res)
        let target_index = -1;
        for (let i = 0; i < testlist2.length; i++) {
            if (testlist2[i] === child) {
                target_index = i;
                break;
            }
        }
        if (target_index === -1) {
            return "";
        }
        res += `:nth-of-type(${target_index + 1})`;
    }
    return res;

}