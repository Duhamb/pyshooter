PAdLib (PyGame [2D] Advanced Graphics Library)
Ian Mallett
March 2008 - January 2013

Introduction:
	PAdLib is the PyGame [2D] Advanced Graphics Library, written by me, Ian Mallett.  It aims to simplify common 2D graphics problems that are encountered while using PyGame.  In fact, PAdLib's draw API (PAdLib.draw) looks very much like the pygame.draw module in PyGame.  PAdLib was developed with Python 3.3.0, but it should be backwards-compatible with Pythons down to 2.6.*.
	
	I probably haven't thought of everything, so please let me know if you think adding a particular new feature would be useful!

	Run and examine the code of the included example files, preferably in order (they're ranked in approximate difficulty), to see how they work.

Installation:
	There is no formal installation procedure.  Because PAdLib is a small library, simply copy the PAdLib folder into your project wherever convenient, and import as demonstrated in the examples.

Contact:
	Email me at ian@geometrian.com (or from my website, geometrian.com) to suggest new ideas or report bugs!

TODO:
	Width argument for pattern lines?
	Soft shadows
	Antialiased circles?  PyGame 2 is expected to have them.  Prerequisite for antialiased rounded rectangles.
	Optional NumPy-based particles

BUGS:
	There *might* be a problem on different architectures, swapping the red and blue channels when drawing in the trianglecustom function, and those that depend on it.
	
Changes:
	v.8.1.0:
		Adds Bézier curves in the PAdLib.bezier module and updates various things, including the demo.  Rearranges drawing functionality to more closely parallel PyGame.  Adds triangle drawing with interpolated colors, custom shading, or textures.  Adds textured quads.
	v.8.0.2:
		Rewrites the shadowing algorithm to be less crufty, after a bug was reported in some edge cases.  Also results in less rasterization, although more complexity.
	v.8.0.1:
		Modules could suffer from import errors if they were named the same.  Fixed internal importing methods.  Revealed PAdLib.occluder.Occluder.intersects(...).  Fixed bug in particles.  Renamed some methods of the emitters, minor fixes in examples.
	v.8.0.0:
		Almost completely rewritten, with a new, more intuitive API.  Removed the AA functionality, because it was unhelpful and slow, renamed a lot of stuff, updated documentation file(s), and reworked all the examples, including merging some and, again, rewriting everything.  Removed slider demo.
	v.7.0.0 (unreleased):
		Minor fixes, changes, optimizations, revisions
	v.6.0.0 (unreleased):
		Added Slider Demo
	v.5.0.0:
		Made Bézier curves [actually cubic splines] curves with n control points, updated relevant demo
		Made the Rounded Rectangles method more efficient and customizable.  Added transparency
	v.4.0.0:
		Added DashedLine() and Demo
		Added BezierCurve()/aaBeizerCurve() and Demo
		Added Particles/Shadows Demo
		Made fewer occluders in Particles Demo
	v.3.0.0:
		Added optional Gravity, Collision Detection, and Bouncing to particle_system()
		Added support for Psyco
	v.2.0.0:
		Added pygame.init() which fixes bug in PyGame 1.7
		Added RoundedRect() and Demo 
	v.1.0.0 - original release:
		Had:
			particle_system()
			Shadow()
			antialias()
			aacircle()

Credits:
	John Eriksson (wmjoers) provided the inspiration for the underlying shadowing code.  Previous versions of this library presented a modified version, but this version takes a completely new tactic.  I regret that I never took the time to fully understand John's algorithm, so I don't know if the one presented here is similar.
	
	Bug reports by the following:
	-Mustafa Furkan Kaptan 
	-Let me know if I have missed you!
	
	Other algorithms are fairly standard, and are cited within the source itself.
	
Legal:
	PAdlib is released under specific terms found on my website (geometrian.com), which you should consult for precise information, but it is generally open source and free.