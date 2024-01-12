# sunrise-equation
Exploring the sunrise equation

The main question I had was whether it's troue that the sunrise and sunset time evolution has a 
slight phase shift, i.e. when the e.g. sunrise starts to happen earlier that the day before, the 
sunset continues to happen earlier than the day before. The answer is yes, this is indeed the 
case.

It is still not intuitively clear why the sunrise and the sunset times could have this phase 
shift. The plots in the notebook show that:
1. The phase shift is evidenced by the shift in the relative positions of the moments when the 
sunrise and sunset times inverse the direction of change.
1. The phase shift is observed around the winter and summer solstice days.
1. The amplitude of the phase shift, as measured from the plots of the derivatives, depends on 
the lattitude of the point. The effect is much stronger near the equator, but zero on the 
equator (see the note below). The effect is almost close to zero near arctic circles for the 
summer solstice, but almost the same for the winter solstice.
1. The amplitude of the phase shift, as measured from the plots of the derivatives, is not equal 
for the winter ands summer solictice and vary by a significantly amount.
1. The effect remains weak in the sense that the absolute and relative change in the 
sunset/sunrise time is very weak near the extremum.
1. It seems to be related to the change in the sun noon position. Indeed, it is correlated with 
the maxima of the sun noon change, it is almost vanishing near arctic circle for the summer 
solstice when the daytime is largest and is much larger than the variation in the sun noon time,
 but is clearly visible for the winter solstice when the days are short, and inversly, is more 
 always pronounced near equator where the day time variation is the weakest.
1. I have no intuitive explanation for the additional structure of the sunrise/sunset time 
derivatives (a double bump between days 200 and 350 for the sunrise, similar for the sunset at 
the beginning of the year), but this should also be related to the jiggling of the sun noon time.
 Indeed, when we approach equator this structure becomes more and more pronounced and finaly the 
 three curves - sunrise, sunset and sun noon times - coincide.

Few helpful links:

[Sunrise equation](https://en.wikipedia.org/wiki/Sunrise_equation) that contains among other the 
Python code used for the simulation.

[Equation of time](https://en.wikipedia.org/wiki/Equation_of_time)

[Equation of Time](https://www.youtube.com/watch?v=Mx9AJJSKIL4) - a YouTube video with a nice and 
clear visualisation of the effects of the Earth's orbit excentiricity and  Earth's axis tilt on 
the duration of the solar day.
