def load_intensity_file(file_name):
    sense = open(file_name, 'r')
    sense_inds = None
    sense_snps = set()
    snp_ind_int = dict()
    flr = False
    for line in sense:
        line = line.strip()
        if(flr == False):
            line = line.replace('"', '')
            line = line.replace('.CEL', '')
            sense_inds = line.split(' ')
            del sense_inds[0]
            for i in xrange(len(sense_inds)):
                sense_inds[i] = sense_inds[i].split('_')[1]
            flr = True
            continue
        cols = line.split()
        snp = cols[0].replace('"', '')
        sense_snps.add(snp)
        if(snp not in snp_ind_int):
            snp_ind_int[snp] = dict()
        for i in range(len(sense_inds)):
            ind = sense_inds[i]
            if(ind not in snp_ind_int[snp]):
                snp_ind_int[snp][ind] = dict()
            snp_ind_int[snp][ind] = float(cols[i+1])
    sense.close()
    return (snp_ind_int, sense_snps, sense_inds)
