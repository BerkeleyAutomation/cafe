#!/usr/bin/env python
#coding=utf-8
import environ
from opinion.opinion_core.models import *
from opinion.opinion_core.modelsMulti import *
import numpy as np
from opinion.includes.queryutils import *
import json
from django.db.models import Q
from django.db.models import *
from django.contrib.auth.models import User

"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1
print json.dumps(counties)
"""
"""
geo_json=open('../geo-ca.json')
geo_data=json.load(geo_json)
counties = {}
for i in range(0,len(geo_data['features'])):
    county=geo_data['features'][i]['properties']['NAME']
    zipcode_in_county=ZipCode.objects.filter(state='CA').filter(county__startswith=county)
    if len(zipcode_in_county) > 0:
        counties[county] = ZipCodeLog.objects.filter(location__in=zipcode_in_county).count()/(geo_data['features'][i]['properties']['Population']/10000.0)
print json.dumps(counties)
"""

"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1

counties2 = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0 and CommentAgreement.objects.filter(is_current=True,rater=u).count() > 5:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties2:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1.0/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
        else:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1.0/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
print json.dumps(counties2)
"""

"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0 and UserRating.objects.filter(is_current=True, user = u).count() > 3:
        m = np.mean(UserRating.objects.filter(is_current=True, user = u).values_list('rating'))
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]].append(m)
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = [m]

counties2 = {}
for c in counties:
    counties2[c] = 1-np.median(counties[c])
print json.dumps(counties2)

"""
"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1

counties2 = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    comment = ""
    if DiscussionComment.objects.filter(user = u,is_current=True).count() > 0:
        c = DiscussionComment.objects.filter(user = u,is_current=True)[0]
        tag_object = AdminCommentTag.objects.filter(comment = c)
        if tag_object.count() > 0:
            comment = tag_object[0].tag.lower()

    if len(zc_log_object) > 0 and (('disaster' in comment)):
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties2:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
        else:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1.0/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
print json.dumps(counties2)
"""


"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    comments = AdminCommentTag.objects.filter(Q(tag__icontains="disaster")).values("comment")
    if len(zc_log_object) > 0 and CommentAgreement.objects.filter(is_current=True, rater = u, comment__in = comments).count() > 0:
        m = np.mean(CommentRating.objects.filter(is_current=True, rater = u, comment__in = comments).values_list('rating'))
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]].append(m)
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = [m]

counties2 = {}
for c in counties:
    counties2[c] = 1-np.median(counties[c])
print json.dumps(counties2)
"""
"""
for r in CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(Q(is_current=True, comment__icontains='water', user__in=User.objects.filter(is_active=True))), is_current=True).order_by('created'):
    if r.agreement != .5:
        print 1-r.agreement
"""


# state = OpinionSpaceStatement.objects.get(statement_number=0)
# state.statement = "La aplicacion de la Ley de Asistencia Asequible ('Obamacare')"
# print(state.statement)
# # state.short_version = "slider"
# state.save()




# state = OpinionSpaceStatement.objects.get(statement_number=1)
# state.statement = "Calidad de la educacion K-12 publicas"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=2)
# state.statement = "Asequibilidad de los colegios y universidades estatales"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=3)
# state.statement = "El acceso a los servicios estatales para los inmigrantes indocumentados"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=4)
# state.statement = "Leyes y reglamentos relativos a la marihuana recreativa"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=5)
# state.statement = "Los derechos de matrimonio para parejas del mismo sexo"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# class Place(Model):
#     name = CharField(max_length=50)
#     address = CharField(max_length=80)

#     def __str__(self):              # __unicode__ on Python 2
#         return "%s the place" % self.name

# class Restaurant(Model):
#     place = OneToOneField(Place, primary_key=True)
#     serves_hot_dogs = BooleanField()
#     serves_pizza = BooleanField()

#     def __str__(self):              # __unicode__ on Python 2
#         return "%s the restaurant" % self.place.name

def translate(comment):
    # validatedComment = validate(comment)
    # return validatedComment
    return "spanish(" + comment + ")"

# firstComment = DiscussionComment.objects.get(id=1)
# firstComment.spanish_comment = "California tiene una de las politicas ambientales mas progresistas de la nacion, debemos trabajar mas para hacer de California un centro internacional de 'tecnologia verde'. Esta inversion equilibra valores de la innovacion y la responsabilidad ambiental de nuestro estado."
# firstComment.original_language = "english"
# firstComment.save()

#firstComment = DiscussionComment.objects.get(id=1)
# print(firstComment.spanish_comment)
# print(firstComment.original_language)


# state = OpinionSpaceStatement.objects.get(statement_number=0)
# state.statement = 'Implementation of the Affordable Care Act ("Obamacare")'
# state.spanish_statement = u"La aplicación de la Ley de Asistencia Asequible ('Obamacare')"
# print(state.statement)
# print(state.spanish_statement)
# state.input_type = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=1)
# state.statement = 'Quality of K-12 public education'
# state.spanish_statement = u"Calidad de la educación K-12 públicas"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=2)
# state.statement = 'Affordability of state colleges and universities'
# state.spanish_statement = u"Asequibilidad de los colegios y universidades estatales"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=3)
# state.statement = 'Access to state services for undocumented immigrants'
# state.spanish_statement = u"El acceso a los servicios estatales para los inmigrantes indocumentados"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=4)
# state.statement = 'Laws and regulations regarding recreational marijuana'
# state.spanish_statement = u"Leyes y reglamentos relativos a la marihuana recreativa"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=5)
# state.statement = 'Marriage rights for same-sex partners'
# state.spanish_statement = u"Los derechos de matrimonio para parejas del mismo sexo"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# super_user = User.objects.get(pk=1)
# print(super_user.username)
# super_user.set_password("crc")
# super_user.save()

# lst = []



good_comments = [384, 1673, 1224, 2261, 2011, 1924, 2159, 1162, 1975, 1308, 922, 1740, 1757, 2423, 1700, 490, 736, 1723, 2406, 1568, 1561, 2327, 855, 1129, 660, 2033, 2506, 2061, 2459, 1647, 663, 689, 672, 773, 1478, 1935, 1206, 1911, 1832, 1318, 1181, 838, 627, 1952, 1463, 396, 905, 1187, 1239, 576, 600, 1513, 1061, 1387, 782, 1270, 1446, 897, 762, 1221, 2394, 2293, 1849, 1490, 785, 545, 723, 754, 1236]

englishComments = ['California is a magnet for artists; however, there is almost no state funding available to support public works of art. California should make greater efforts to support the arts.', 'Child care is expensive for most working parents. California should improve its availability of affordable, fully trained, reliable, and licensed child care.', 'Towns like Oakland do not have enough police officers to protect the large community. Thus, the residents of large cities are at risk of more violent crime. California should help large cities keep its residents safe by hiring more police officers.', 'California should repeal the death penalty. It should be used very rarely, if at all, and must not be barbaric.', 'California is one of the most ethnically and nationally diverse societies on earth. California should continue to promote diversity, social mobility, and economic opportunity for all Californians.', 'We need to do more to bring new businesses to California.', 'Current legislation can cause businesses to leave California. The law should foster commercial activity to retain businesses within the state.', 'California should provide more affordable job training for unemployed workers.', 'Local communities should be able to raise revenue for local concerns, such as the police department and schools, without being withheld by the almost impossible two-thirds, supermajority vote threshold.', 'The unfunded state employee pension liability is nearly $80 billion. Until properly funded, the large liability threatens state employee retirees and our credit rating. California should improve its management of pensions for state employees.', 'California should provide tax breaks to small businesses that employ prison parolees.', 'California should provide preschool access for all children.', 'As a state that has benefitted from cutting-edge innovation and creativity, California should recognize the need and value of arts education by investing more dollars in this sector of public education.', "California's teacher tenure laws have been declared unconstitutional by the Los Angeles Superior Court. California school districts should be allowed to fire poorly performing teachers.", 'Studies have shown a strong, direct correlation between poor nutrition and poor school performance. California should increase its investment in nutrition programs to improve student achievement.', 'Using new technology and social media in the classroom can lead to better educational outcomes.', 'Not all high school students are college bound. California needs to invest in improving access to vocational training for high school students through classes, apprenticeships, or partnerships with community colleges.', 'To reduce carbon emissions, California should increase our use of nuclear power.', 'California has compromised many ecosystems by damming rivers, converting forests to farms and sending delta water to the deserts of the Central Valley. California is not doing enough to preserve nature and wildlife.', 'California should encourage the growth of alternative energy such as solar power.', 'Fracking may have caused the drought, contaminated groundwater, contributed to climate change, and could possibly cause earthquakes. These environmental consequences are all reasons to ban fracking.', 'California has implemented a cap-and-trade system that can reduce greenhouse gas emissions by regulating the market and encouraging the use of clean energy.', 'There is a trade-off between economic development, affordable housing, and protection of the environment in urban planning. California should balance these aspects in urban planning.', "California's water infrastructure is aging. California should increase its efforts to develop de-salinization and alternative water sources.", 'We must be aware of toxins in our water sources. California must be stricter on its allowance of toxins in the water sources.', 'Large campaign contributions can have negative impacts on political campaigns. California should limit campaign contributions.', 'Local government is often the first line of contact for residents. California should increase its provision of state services at the local level.', 'Tighter oversight of the sources and uses of political contributions would reduce access of politicians to the temptations of power. California should improve the transparency of political contributions.', 'Government needs to engage its citizens, measure program performance, and be accountable for reaching stated goals and objectives.', 'With over 6,000 people shot in California each year, of which nearly half die, creating stricter gun laws is vitally important to saving lives.', 'School shootings are an avoidable tragedy. California should develop programs and laws to keep children safe from school shootings.', 'Lack of access and affordability of mental health services has a detrimental effect not only on the people affected by mental illness but also on the economy and quality of life of others.', "California obesity rates are expected to double to over 44% of the state's population by 2030. California should increase the availability of nutrition and physical education in K-12 education to stop obesity of young Californians.", 'The eventual rise of the number of seniors dependent on the government for medical and financial support will create debt for the state and negatively impact the quality of care of seniors. California should increase the availability of housing and services for seniors.', '50,000 Californians die every year from smoking along with 5,000 non-smokers exposed to second-hand smoke. California should improve efforts to eliminate smoking in public areas.', 'It may be helpful to have state support for local municipalities to help people who are homeless or struggling with insecure housing.', 'We need an open border for Mexican nationals in honor of our history, and also for our economy.', 'Many rural areas in California have no, limited, or expensive access to Broadband Internet. The state should provide Internet to all areas of California.', 'It is now becoming more commonplace for governments to record large quantities of data. California should increase government transparency and publish the uses of the data collected.', 'Many California state online services are outdated. California should modernize government online services to increase access to state offices and agencies.', 'Improving workplace safety protections and collective bargaining rights is an important issue for many Californians.', 'Government involvement with leadership programs in underprivileged communities is important.', 'California is home to one of the largest populations of members of the US military. California should improve its plan to support veterans and military personnel.', 'Raising the California minimum wage is a necessary step to ensure Californian families have a decent standard of living and their children have access to education and opportunity.', 'As Detroit has demonstrated, our state may need to reconsider its position on pensions. Although no one should have their pre-existing promises voided, there is potential for future contracts to include a different set of benefits. California should reform its pension program to be sustainable.', 'Violence against women, including domestic violence and sexual assault, is an issue in California. California should support survivors and prosecute perpetrators of this type of violence.', 'California prisons and jails are overcrowded and over-represented by minorities and people with mental health needs. California should enact government programs for prevention and improve release programs.', 'Police brutality and corruption can be prevented with more oversight.', 'California should be taking greater measures to protect the privacy and personal data of its residents.', 'Proposition 13 limits the amount of property tax individuals and businesses must pay. California should repeal Prop 13 for businesses.', "Term limits for state representatives. California's current limit for terms is 12 years from Prop 28, which passed in 2012. This should be increased.", 'Support for public libraries is important because they are the chief vehicles for public literacy after the completion of formal education.', 'Tax breaks should be given to companies and individuals that make environmental improvements.', 'We need to develop ways of travel that are efficient and affordable for all individuals with the lowest impact on the global environment. California should continue to develop public transportation.', 'More and more Californians are choosing to ride their bicycles to exercise and commute. This has also led to more cycling accidents/deaths. California can make roads safer for cyclists by adding bike lanes.', 'High speed rail will result in many great outcomes: the number of cars on the road will be reduced and transportation will be less congested. California should continue its implementation of the high speed rail.', 'Unequal speed limits for trucks and cars is unsafe for all drivers.', 'California should do more for unincorporated urban areas such as the areas in Los Angeles County that are not incorporated as the City of Los Angeles is. ', 'California should increase its efforts to rehabilitate the homeless and have them join the workforce.', 'Comprehension of initiatives is central to the link between voters and intended outcome of voting. California should use plain language on voter ballots.', 'Low voter registration rates and low rates of voting among registered voters undermine the democratic system we all are so proud of. California should do more to encourage voter turnout.', 'Large agribusiness firms purchase water supplied by public agencies, and resell this water on the open market for profits. We should remove all subsidies on commercial water use, and require private businesses to pay the full cost of delivering the water.', 'We are currently in a drought and water conservation in urban areas and agricultural industry is important.', 'Climate change will lead to extreme weather and rising sea levels. California should do more to stop climate change.', 'Being located in earthquake country, California will inevitably experience large, devastating seismic events in the future. California should increase the seismic safety of its buildings and do more to prepare its residents.', 'California should create a fund or take other measures to help mitigate threats related to sea level rise, earthquakes, and wildfires.', 'California is currently in a drought. California should create a better water conservation plan.', 'California should do more to alleviate effects of the drought.', 'Water is important to the environment, working families, agriculture, the economy, and recreation. California should do more to manage the drought.']

spanishComments = ['California es un lugar atractivo para los artistas; sin embargo, casi no existen fondos estatales para apoyar trabajos art\xc3\xadsticos p\xc3\xbablicos. California deber\xc3\xada hacer mayores esfuerzos en apoyar las artes.', 'El cuidado de ni\xc3\xb1os es costoso para la mayor\xc3\xada de los padres trabajadores. California deber\xc3\xada mejorar la disponibilidad de servicios de guarder\xc3\xadas que cuenten con licencia, est\xc3\xa9n plenamente capacitados, sean accesibles y al mismo tiempo confiables.', 'Ciudades, como Oakland, no tienen suficientes agentes de polic\xc3\xada para proteger a la poblaci\xc3\xb3n. En consecuencia, los residentes de grandes ciudades, como esta, se ven expuestos a actos violentos de delincuencia. California deber\xc3\xada ayudar a las grandes ciudades a preservar la seguridad de sus residentes mediante la contrataci\xc3\xb3n de m\xc3\xa1s polic\xc3\xadas.', 'California deber\xc3\xada derogar la pena de muerte. Esta deber\xc3\xada utilizarse rara vez, si se diera el caso, y no debe ser violenta.', 'California es una de las sociedades m\xc3\xa1s pluralistas del mundo, considerando su diversidad \xc3\xa9tnica y de nacionalidades. California deber\xc3\xada seguir promoviendo la diversidad, la movilidad social y las oportunidades econ\xc3\xb3micas para todos los californianos.', 'Tenemos que esforzarnos m\xc3\xa1s en atraer nuevos negocios a California.', 'La legislaci\xc3\xb3n actual puede causar la salida de empresas de California. Las leyes deber\xc3\xadan fomentar la actividad comercial para retener negocios dentro del estado.', 'California deber\xc3\xada proporcionar capacitaci\xc3\xb3n laboral m\xc3\xa1s accesible a trabajadores desempleados.', 'Las comunidades locales deber\xc3\xada poder generar ingresos para cubrir necesidades de inter\xc3\xa9s general, como el departamento de polic\xc3\xada y escuelas, sin que el dos tercios de estos les sean retenidos.', 'El pasivo de las obligaciones pensionales para los empleados estatales asciende a casi $80 billones. Hasta no financiarlo adecuadamente, este gran pasivo amenaza a jubilados estatales as\xc3\xad como tambi\xc3\xa9n nuestra calificaci\xc3\xb3n crediticia. California deber\xc3\xada mejorar su manejo de pensiones para empleados estatales.', 'California deber\xc3\xada ofrecer ventajas fiscales a peque\xc3\xb1as empresas que emplean a personas en libertad condicional.', 'California deber\xc3\xada facilitar el acceso preescolar a todos los ni\xc3\xb1os.', 'Como estado que se ha beneficiado de la innovaci\xc3\xb3n de vanguardia y la creatividad, California deber\xc3\xada reconocer la necesidad y el valor de la educaci\xc3\xb3n art\xc3\xadstica, invirtiendo m\xc3\xa1s dinero en este sector de la educaci\xc3\xb3n p\xc3\xbablica.', 'La ley de antiguedad de maestros de California ha sido declarada inconstitucional por la Corte Superior de Los Angeles. Los distritos escolares de California deber\xc3\xada estar autorizados a despidir a maestros con bajo rendimiento.', 'Los estudios han demostrado una fuerte y directa correlaci\xc3\xb3n entre la mala nutrici\xc3\xb3n y el bajo rendimiento escolar. California deber\xc3\xada aumentar su inversi\xc3\xb3n en programas de nutrici\xc3\xb3n que permitan mejorar el rendimiento estudiantil.', 'El uso de las nuevas tecnolog\xc3\xadas y las redes sociales en el aula podr\xc3\xadan conducir a mejores resultados educativos.', 'No todos los estudiantes apuntan a asistir a los colleges una vez finalizados sus estudios secundarios. California necesita invertir en mejorar el acceso a programas de formaci\xc3\xb3n profesional atrav\xc3\xa9s de clases, per\xc3\xadodos de pasant\xc3\xadas, o asociaciones con colleges comunitarios.', 'Para reducir las emisiones de carbono, California deber\xc3\xada aumentar el uso de energ\xc3\xada nuclear.', 'California ha puesto en peligro muchos ecosistemas mediante la represa de r\xc3\xados, la transformaci\xc3\xb3n de bosques en granjas y el envio de agua del delta a los desiertos del Central Valley. California no est\xc3\xa1 haciendo lo suficiente para preservar la naturaleza y la vida silvestre.', 'California debe fomentar el crecimiento de energ\xc3\xadas alternativas como la energ\xc3\xada solar.', 'Fracking podr\xc3\xada haber causado sequ\xc3\xadas, contaminado el agua subterr\xc3\xa1nea, contribuido al cambio clim\xc3\xa1tico, y causado terremotos. Estas consecuencias ambientales son justificadas razones para prohibir el Fracking.', 'California ha implementado un sistema de cap-and-trade capaz de reducir las emisiones de gases de efecto invernadero mediante la regulaci\xc3\xb3n del mercado y el fomento del uso de energ\xc3\xada limpia.', 'En la planificaci\xc3\xb3n urbana existe una compensaci\xc3\xb3n entre el desarrollo econ\xc3\xb3mico, las viviendas accesibles, y la protecci\xc3\xb3n del medio ambiente. California deber\xc3\xada equilibrar estos aspectos en la planificaci\xc3\xb3n urbana.', 'La infraestructura de agua de California est\xc3\xa1 quedando obsoleta. California deber\xc3\xada redoblar esfuerzos para desarrollar planes de desalinizaci\xc3\xb3n y fuentes alternativas de agua.', 'Debemos ser conscientes de las toxinas en nuestras fuentes de agua. California debe ser m\xc3\xa1s estrictas en sus controles de toxinas en las fuentes de agua.', 'Las grandes contribuciones en campa\xc3\xb1as electorales pueden tener effectos negativos. California deber\xc3\xada limitar las contribuciones durante las campa\xc3\xb1as electorales.', 'El gobierno local es a menudo la primera l\xc3\xadnea de contacto de los residentes. California deber\xc3\xada incrementar la provisi\xc3\xb3n de servicios estatales a nivel local.', 'Una supervisi\xc3\xb3n m\xc3\xa1s estricta de las fuentes y usos de las contribuciones pol\xc3\xadticas reducir\xc3\xadan el acceso de pol\xc3\xadticos a las tentaciones del poder. California deber\xc3\xada transparentar mejor las contribuciones pol\xc3\xadticas.', 'El gobierno necesita involucrar a sus ciudadanos, medir el desempe\xc3\xb1o de programas, y rendir cuentas para as\xc3\xad alcanzar la metas y objetivos establecidos.', 'Con m\xc3\xa1s de 6.000 personas al a\xc3\xb1o heridas por armas de fuego en California, de las cuales cerca de la mitad mueren, la creaci\xc3\xb3n de una estricta legislaci\xc3\xb3n sobre el uso de armas es de vital importancia para salvar vidas.', 'Los tiroteos en las escuelas son una tragedia evitable. California deber\xc3\xada desarrollar programas y leyes que protejan de estos episodios a los ni\xc3\xb1os en las escuelas.', 'La falta de acceso y la asequibilidad a los servicios de salud mental tiene un efecto perjudicial no s\xc3\xb3lo para las personas afectadas por una enfermedad mental, sino tambi\xc3\xa9n en la econom\xc3\xada y calidad de vida de los dem\xc3\xa1s.', 'Se espera que las tasas de obesidad de la poblaci\xc3\xb3n de California se duplique en m\xc3\xa1s del 44% para el 2030. California deber\xc3\xada aumentar los programas de nutrici\xc3\xb3n y la educaci\xc3\xb3n f\xc3\xadsica en la escuelas K-12 con el objectivo de detener la obesidad de los j\xc3\xb3venes californianos.', 'El eventual aumento en el n\xc3\xbamero de personas mayores dependientes de apoyo m\xc3\xa9dico y econ\xc3\xb3mico del gobierno crear\xc3\xa1 una deuda para el estado e impactar\xc3\xa1 negativamente en la calidad de la atenci\xc3\xb3n a los ancianos. California deber\xc3\xada incrementar la dispinibilidad de viviendas y servicios para personas mayores.', 'Cada a\xc3\xb1o 50.000 californianos mueren por fumar, adem\xc3\xa1s de otros 5.000 por estar expuestos al humo de los cigarrillos. California deber\xc3\xada mejorar sus esfuerzos por eliminar el tabaquismo de las zonas p\xc3\xbablicas.', 'Podr\xc3\xada ser beneficioso para los municipios contar con el apoyo del estado en la ayuda a personas sin techo o en situaciones de viviendas inestables.', 'Necesitamos una frontera abierta para mexicanos nacionalizados en honor a nuestra historia, y tambi\xc3\xa9n para el beneficio de nuestra econom\xc3\xada.', 'Muchas zonas rurales de California carecen de acceso a Internet, o este es limitado o muy costoso. El estado deber\xc3\xada proveer Internet a todas las \xc3\xa1reas de California.', 'Es cada vez m\xc3\xa1s com\xc3\xban que los gobiernos almacenen grandes cantidades de datos sobre los ciudadanos. California deber\xc3\xada aumentar la transparencia guvernamental y publicar el uso de los datos colectados.', 'Varios servicios online del estado de California est\xc3\xa1n desactualizados. California deber\xc3\xada modernizar los servicios online del gobierno para aumentar el acceso a las oficinas y agencias estatales.', 'Mejorar la seguridad en los ambientes de trabajo y los derechos de negociaci\xc3\xb3n de convenios colectivos es un tema importante para muchos californianos.', 'Es importante que el gobierno promueva programas de liderazgo en comunidades de escasos recursos.', 'En California reside una gran poblaci\xc3\xb3n de miembros de las fuerzas armadas de los Estados Unidos. California deber\xc3\xada mejorar su plan de apoyo a veteranos y personal militar.', 'Aumentar el salario m\xc3\xadnimo en California es un paso necesario para asegurar que las familias californianas tengan un est\xc3\xa1ndar de vida digno y para que sus hijos gozen de educaci\xc3\xb3n y oportunidades.', 'As\xc3\xad como Detroit, nuestro estado deber\xc3\xada reconsiderar su posici\xc3\xb3n sobre las pensiones. Aunque a nadie deber\xc3\xadan anularle los beneficios que ya les fueron concedidos, existe la posibilidad de que futuros contratos incluyan diferentes conjuntos de beneficios. California deber\xc3\xada reforma su programa de pensi\xc3\xb3n para hacerlo sustentable. ', 'La violencia contra las mujeres, incluyendo la violencia dom\xc3\xa9stica y el abuso sexual, es un problema en California. California deber\xc3\xada apoyar a las sobrevivientes y enjuiciar a aquellos que hayan incurrido en este tipo de actos.', 'Las prisiones y c\xc3\xa1rceles en California estan abarrotadas y sobre-representadas por minor\xc3\xadas y personas con transtornos mentales. California deber\xc3\xada promulgar programas gubernamentales de prevenci\xc3\xb3n y mejorar los programas de liberaci\xc3\xb3n.', 'La brutalidad policial y la corrupci\xc3\xb3n se pueden prevenir con una mayor supervisi\xc3\xb3n.', 'California deber\xc3\xada adoptar mejores medidas para proteger la privacidad y los datos personales de sus residentes.', 'La propuesta 13 regula la cantidad de impuestos que personas y empresas deben pagar sobre los inmuebles. California deber\xc3\xada derogar la propuesta 13 en el caso de empresas.', 'L\xc3\xadmite de mandato para los representantes del estado. De acuerdo a la propuesta 28 aprobada en 2012 el tiempo m\xc3\xa1ximo de mandato en la actualidad es de 12 a\xc3\xb1os. Esto deber\xc3\xada ser incrementado.', 'El apoyo a las bibliotecas p\xc3\xbablicas es importante, ya que estas representan los medios principales para a la alfabetizaci\xc3\xb3n p\xc3\xbablica una vez finalizada la educaci\xc3\xb3n formal.', 'Incentivos fiscales deben ser concedidos a empresas e individuos que promueven mejoras ambientales.', 'Necesitamos desarrollar maneras de viajar que sean eficientes, de bajo impacto ambiental y al mismo tiempo asequibles para la mayor parte de la poblaci\xc3\xb3n. California deber\xc3\xada continuar desarrollando el transporte p\xc3\xbablico.', 'Cada vez m\xc3\xa1s los californianos est\xc3\xa1n optando por usar bicicletas para hacer ejercicio e ir al trabajo. Esto tambi\xc3\xa9n ha\xc2\xa0llevado\xc2\xa0a m\xc3\xa1s accidentes y muertes associados al ciclismo. California puede hacer carreteras m\xc3\xa1s seguras para ciclistas mediante la adici\xc3\xb3n de ciclov\xc3\xadas. ', 'El tren\xc2\xa0de alta\xc2\xa0velocidad trear\xc3\xa1 grandes resultados: el numero de coches en las carreteras se reducir\xc3\xa1 y el transporte estar\xc3\xa1 menos congestionado. California debe continuar su implementaci\xc3\xb3n de trenes de alta velocidad.', 'Los l\xc3\xadmites de velocidad diferenciados para camiones y coches son peligrosos para los conductores.', 'California deber\xc3\xada hacer m\xc3\xa1s esfuerzos por las zonas urbanas no atendidas, tales como las \xc3\xa1reas del\xc2\xa0Condado\xc2\xa0de Los Angeles que no son tan atendidas como la ciudad de Los Angeles.', 'California debe mejorar sus esfuerzos por rehabilitar a las personas sin hogar y ayudarlos a integrarse mundo laboral.', 'La comprensi\xc3\xb3n de las iniciativas electorales es fundamental para fomentar la relaci\xc3\xb3n entre los votantes y los resultados previstos de la votaci\xc3\xb3n. California debe utilizar un lenguaje sencillo en las boletas electorales.', 'Las bajas tasas de inscripci\xc3\xb3n de electores as\xc3\xad como tambi\xc3\xa9n la baja participaci\xc3\xb3n de los electores registrados, debilita  el sistema democr\xc3\xa1tico que tanto nos enorgullece. California debe hacer mayores esfuerzos para fomentar la participaci\xc3\xb3n electoral.', 'Grandes empresas agroindustriales compran agua suministrada por los organismos p\xc3\xbablicos, y revenden esta agua en el mercado para lucrar. Debemos eliminar todos los subsidios al uso de comercial del agua, y exigir a las empresas privadas a pagar el costo total por la entrega del agua.', 'Actualmente nos encontramos en un estado de sequ\xc3\xada donde la conservaci\xc3\xb3n del agua en zonas urbanas as\xc3\xad como tambi\xc3\xa9n en la industria agr\xc3\xadcola es importante.', 'El cambio clim\xc3\xa1tico causar\xc3\xa1 fen\xc3\xb3menos meteorol\xc3\xb3gicos extremos y una subida del nivel del mar. California debe hacer mayores esfuerzos para detener el cambio clim\xc3\xa1tico.', 'Localizado en area susceptible a los terremotos, California inevitablemente experimentar\xc3\xa1 grandes y devastadores eventos s\xc3\xadsmicos en el futuro. California debe aumentar la seguridad s\xc3\xadsmica de los edificios y hacer mayores esfuerzos para preparar a sus residentes.', 'California debe crear un fondo o tomar otras medidas para ayudar a mitigar las amenazas relacionadas a la subida del nivel del mar, los terremotos y los incendios forestales.', 'California esta pasando por un per\xc3\xadodo de sequ\xc3\xada por lo que debe crear un mejor plan de conservaci\xc3\xb3n del agua.', 'California deber\xc3\xada hacer mayores esfuerzos para aliviar los efectos de la sequ\xc3\xada.', 'El agua es importante para el medio ambiente, las familias trabajadoras, la econom\xc3\xada, y la recreaci\xc3\xb3n. California deber\xc3\xada hacer mayores esfuerzos para manejar la sequ\xc3\xada.']

# print(len(good_comments))
# print(len(englishComments))
# print(len(spanishComments))


# indices = [2,7,23,54,42,62,10,20]
# for index in range(0,len(good_comments)):
#     print('index:' + str(index))
#     pid = good_comments[index]
#     print('id' + str(pid))
#     print('english: ' + englishComments[index])
#     print('spanish: ' + spanishComments[index])
#     print
#     print

# idMap = {}
# for num in range(0,len(good_comments)):
#     idMap[good_comments[num]] = englishComments[num], spanishComments[num]


# cache = []
# for comment in DiscussionComment.objects.all():
#     theId = comment.user.id
#     if comment.user.id in good_comments:
#         print
#         print
#         print(comment.comment)
#         comment.comment = idMap[theId][0]
#         print
#         print
#         print(comment.comment)
#         print
#         print
#         print(comment.spanish_comment)
#         comment.spanish_comment = idMap[theId][1]
#         print
#         print
#         print(comment.spanish_comment)
#         cache.append(theId)
#         comment.blacklisted = False;
#         comment.save()
#     else:
#         comment.blacklisted = True
#         comment.save()

# antiCache = []
# for item in good_comments:
#     if item not in cache:
#         antiCache.append(item)
# print(antiCache)

for obj in Settings.objects.all():
    print('KEY:' + obj.key)
    print('VALUE:' + obj.value)
    


