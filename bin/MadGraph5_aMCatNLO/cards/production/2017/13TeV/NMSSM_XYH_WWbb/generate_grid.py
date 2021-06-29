import os

# the prototype name of the production folder
prod_proto = "NMSSM_XYH_WWbb_MX_{0}_MY_{1}"

### things to replace are
### TEMPLATEMH02 [mX]
### TEMPLATEMH03 [mY]

def change_cards(cardname, replacements):
    
    ## first make a backup copy
    bkpname = cardname + '.bak'
    os.system('mv %s %s' % (cardname, bkpname))

    # edit the file
    fin  = open(bkpname, 'r')
    fout = open(cardname, 'w')

    for line in fin:
        for key, rep in replacements.items():
            line = line.replace(key, rep)
        fout.write(line)

    fin.close()
    fout.close()

    ## delete the backup file
    os.system('rm %s' % bkpname)


def do_point(mx, my):
    # 1 - create the folder
    folder = prod_proto.format(mx, my)
    if os.path.isdir(folder):
        print " >> folder", folder, "already existing, forcing its deletion"
        os.system('rm -r %s' % folder)
    os.system('mkdir ' + folder)
    
    # 2 - copy the original files
    template_flrd = 'Template'
    
    run_card      = 'run_card.dat'
    proc_card     = 'proc_card.dat'
    # param_card    = 'param_card.dat'
    extramodels   = 'extramodels.dat'
    customizecard = 'customizecards.dat'
    
    # to_copy = [run_card, proc_card, param_card, extramodels, customizecard]
    to_copy = [run_card, proc_card, extramodels, customizecard]

    for tc in to_copy:
        os.system('cp %s/%s %s/%s_%s' % (template_flrd, tc, folder, folder, tc) )

    replacements = {
        'TEMPLATEMH03' : str(mx),
        'TEMPLATEMH02' : str(my),
    }

    # 3 - edit in place the cards
    # change_cards('%s/%s_%s' % (folder, folder, param_card), replacements)
    change_cards('%s/%s_%s' % (folder, folder, customizecard), replacements)
    change_cards('%s/%s_%s' % (folder, folder, proc_card), replacements)

    dir_levels = os.getcwd().split('/')
    mg5_dir = ''
    genprod_dir = ''
    genprod_flag = False
    for d in dir_levels:
        mg5_dir += d+'/'
        if not genprod_flag: genprod_dir += d+'/'
        if d == 'MadGraph5_aMCatNLO': break
        elif d == 'genproductions': genprod_flag = True

    os.system("sed 's/TEMPYMASS/%s/g' Template/fragment.py | sed 's/TEMPXMASS/%s/g' | sed 's&TEMPDIR&%s&g' > %s/%s_cfg.py"%(my,mx,mg5_dir,genprod_dir+'genfragments/ThirteenTeV/NMSSM_XYH_WWbb',folder))
####################################################################################

## mX, mY
points = [
    (1500,300),
    (2200,450)
]

for p in points:
    print '... generating', p
    do_point(*p)

