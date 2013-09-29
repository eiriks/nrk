# coding: utf-8

## Tatt fra https://github.com/eiriks/samstemmer/blob/master/fylkesperspektiv/models.py
class Lix(models.Model):
    """LIX pr person basert på den teksten vi finner
- http://sv.wikipedia.org/wiki/LIX
- http://www.sprakrad.no/nb-NO/Toppmeny/Publikasjoner/Spraaknytt/Arkivet/2005/Spraaknytt_1-2_2005/Avisspraak/
< 30 Mycket lättläst, barnböcker
30 - 40 Lättläst, skönlitteratur, populärtidningar
40 - 50 Medelsvår, normal tidningstext
50 - 60 Svår, normalt värde för officiella texter
> 60 Mycket svår, byråkratsvenska
"""
    person = models.ForeignKey(Personer, unique=True)
    dato = models.DateField(auto_now=True) # when this LIX was computed
    materiale = models.CharField(max_length=300) # basert på: "35 spørsmål"
    value = models.DecimalField(max_digits=5, decimal_places=2) # 999.99 her tror jeg jeg vil begrense til to desimaler
    def __unicode__(self):
        return u'%s har lix %s etter %s, regnet den, %s. ' % (self.person, self.value, self.materiale, self.dato)
    # class Meta:
    # unique_together = ("votering", "vedtak_nummer")
