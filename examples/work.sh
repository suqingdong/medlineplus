mkdir -p logs/{gene,condition}

for suffix in {a..z};do
echo "PYTHONPATH=.. python3 -m medlineplus.bin.__init__ gene -s $suffix -o gene/$suffix &> logs/gene/$suffix.log"
done > gene.jobs

for suffix in 0 {a..z};do
echo "PYTHONPATH=.. python3 -m medlineplus.bin.__init__ condition -s $suffix -o condition/$suffix &> logs/condition/$suffix.log"
done > condition.jobs

nohup parallel -j8 < gene.jobs &> /dev/null &
nohup parallel -j8 < condition.jobs &> /dev/null &

cat gene/*.jl > GHR.gene.jl
cat condition/*.jl > GHR.condition.jl

# export xml file
PYTHONPATH=.. python3 -m medlineplus.bin.__init__ gene -s z -o z.gene -O xml
PYTHONPATH=.. python3 -m medlineplus.bin.__init__ condition -s z -o z.condition -O xml
