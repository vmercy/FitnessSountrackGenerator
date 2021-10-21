import gtts
from playsound import playsound
from time import sleep
from pydub import AudioSegment
from pydub.playback import play

tts = gtts.gTTS('Récupération', lang='fr')
tts.save('repos.mp3')

circuitNames = [
  'Cuisses et fessiers',
  'Abdos',
  'Cardio',
  'Tonification complète sans matériel',
]

circuits = [
    [
        ('squats', 30, 30),
        ('fentes côté droit', 20, 0),
        ('fentes côté gauche', 20,20),
        ('squats sumo', 40,20),
        ('fentes croisées côté droit',20,0),
        ('fentes croisées côté gauche',20,20),
        ('levés de jambes',40,20),
        ('fentes sautées',30,30),
        ('extension des mollets',40,20),
        ('squats sautés',40,20),
        ('soulevés de fesses',40,20),
        ('extensions jambe bras',40,20),
        ('levés de jambes latéral',40,20),
        ('chaise',40,20)
    ],
    [
        ('mountain climbers lent sur les tapis', 40, 20),
        ('planche', 40, 20),
        ('planche côté droit',20,0),
        ('planche côté gauche',20,20),
        ('abdos sit-up',40,20),
        ('ciseaux',40,20),
        ('abdos crunch',40,20),
        ('abdos croisés',40,20),
        ('levés de jambe droite',20,0),
        ('levés de jambe gauche',20,20),
        ('planche dynamique',40,20),
        ('rameur',40,20),
        ('abdos touche-talon',40,20),
        ('abdos essuie-glace',40,20),
    ],
    [
      ('mountain climbers', 40,20),
      ('planche spiderman',40,20),
      ('mogul jump',40,20),
      ('burpees',40,20),
      ('talons fesses dynamiques',40,20),
      ('montée de genoux',40,20),
      ('jumping jack',40,20),
      ('corde à sauter',40,20),
      ('pompes',40,20),
      ('kick',40,20),
      ('pas du patineur',40,20),
      ('fractionné',40,20),
    ],
    [
      ('pompes sur genoux',40,20),
      ('crunch inversé',40,20),
      ('burpees',40,20),
      ('ciseaux côté droit',20,0),
      ('ciseaux côté gauche',20,20),
      ('crunch croisé',40,20),
      ('planche',40,20),
      ('jumping jack',40,20),
      ('mountain climbers',40,20),
      ('overhead squat',40,20),
      ('soulevée de fesses',40,20),
      ('fentes sautées',40,20),
      ('planche côté droit',20,0),
      ('planche côté gauche',20,20)
    ],
]

beginningShift = 10


for indexCircuit, circuit in enumerate(circuits):
  tts = gtts.gTTS('Série numéro %s : %s'%(indexCircuit+1, circuitNames[indexCircuit]),lang='fr')
  tts.save('tts/%s.mp3'%indexCircuit)
  for indexExo, exercise in enumerate(circuit):
    exoName = exercise[0]
    tts = gtts.gTTS('Prochain exercice : '+exoName, lang='fr')
    tts.save('tts/%s_%s.mp3'%(indexCircuit,indexExo))

print('Exercices announcements have been generated with success')

loop = AudioSegment.from_mp3('music.mp3')
bell = AudioSegment.from_mp3('countdown.mp3')
bell = bell.apply_gain(5)
repos = AudioSegment.from_mp3('repos.mp3')
repos = repos.apply_gain(10)

timePos = beginningShift
for indexCircuit, circuit in enumerate(circuits):
  circuitSpeech = AudioSegment.from_mp3('tts/%s.mp3'%indexCircuit)
  circuitSpeech = circuitSpeech.apply_gain(10)
  loop = loop.overlay(circuitSpeech, position=1000*(timePos-len(circuitSpeech)//1000-5))
  for indexExercise,exercise in enumerate(circuit):
    exoName = exercise[0]
    duration = exercise[1]
    pause = exercise[2]
    exoSpeech = AudioSegment.from_mp3('tts/%s_%s.mp3'%(indexCircuit,indexExercise))
    exoSpeech = exoSpeech.apply_gain(10)
    loop = loop.overlay(exoSpeech, position=1000*(timePos-len(exoSpeech)//1000-2))
    loop = loop.overlay(bell, position=1000*(timePos)) #debut exercice
    timePos+=duration
    if pause:
      loop = loop.overlay(bell, position=1000*(timePos)) #debut repos
      loop = loop.overlay(repos, position=1000*(timePos-len(repos)//1000))
      timePos+=pause
  timePos+=beginningShift

print('Audio file has been generated with success')
loop.export('CIRCUITS_SP07.mp3',format='mp3')
#play(loop)
