FILES=`ls ap90*.*`

for F in $FILES
 do
 G="${F//ap90/bur}"
 cmd="mv $F $G"
 echo $cmd
 $cmd
 done
