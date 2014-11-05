import gvar as gv
import numpy as np
path="./data-files"
path2="./cov-files"
file1="data-out-small2";
file2="data-out-med2";
diff_file="cov-test-diff";
mag_file1="cov-test-mag1";
mag_file2="cov-test-mag2";

ds1 = gv.dataset.Dataset(path+'/'+file1);
ds2 = gv.dataset.Dataset(path+'/'+file2);
ad1 = gv.dataset.avg_data(ds1);
ad2 = gv.dataset.avg_data(ds2);
cv1 = gv.evalcov(ad1)[('Gaa','Gaa')];
cv2 = gv.evalcov(ad2)[('Gaa','Gaa')];
scv = (cv1 - cv2)/(cv1 + cv2);
f = open(path2+'/'+diff_file,'w');
f.write("# "+file1+' '+file2+'\n');
for j in range(48):
 f.write(' '.join(str(scv[i][j]) for i in range(48)) + '\n');
f.close();
f = open(path2+'/'+mag_file1,'w');
f.write("# "+file1+'\n');
for j in range(48):
 f.write(' '.join(str('{:e}'.format(cv1[i][j]/ad1['Gaa'][j].mean)) for i in range(48)) + '\n');
f.close();
f = open(path2+'/'+mag_file2,'w');
f.write("# "+file2+'\n');
for j in range(48):
 f.write(' '.join(str('{:e}'.format(cv2[i][j]/ad2['Gaa'][j].mean)) for i in range(48)) + '\n');
f.close();
