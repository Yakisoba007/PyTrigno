def bisp3cum(signal, samprate, maxlag=0, window=None, scale=None):
    
    #	BISP3CUM Auto bispectrum/3rd order cumulant
    #
    #	[bisp,freq,cum,lag]=bisp3cum(signal,samprate,maxlag,window,scale)
    #
    #	The maxlag*2+1 x maxlag*2+1 element auto bispectrum and 3rd order cumulant matrices
    #	and maxlag*2+1 element frequency and lag vectors are computed from the signal
    #	matrix containing samples in rows and records in columns, signal sample rate and
    #	maximum lag scalars, and lag window function and scale strings.
    #
    #	If unspecified, the signal matrix is entered after the prompt from the keyboard,
    #	and the default assignments samprate=1 and maxlag=0 are used.  The window and scale
    #	strings specify lag window and scale matrix computation, according to:
    #
    #	window = 'none', 'n', or unspecified does not compute a window
    #	       = 'uniform' or 'u' computes the uniform hexagonal window
    #	       = 'sasaki' or 's' computes the sasaki window
    #	       = 'priestley' or 'p' computes the priestley window
    #	       = 'parzen' or 'pa' computes the parzen window
    #	       = 'hamming' or 'h' computes the hamming window
    #	       = 'gaussian' or 'g' computes the gaussian distribution window
    #	       = 'daniell' or 'd' computes the daniell window
    #
    #	scale  = 'biased', 'b', or unspecified computes the biased estimate
    #	       = 'unbiased' or 'u' computes the unbiased estimate
    
    #	Implemented using MATLAB 5.3.1 and additional functions:
    #
    #	mat=toep(column,row)
    #	wind=lagwind(lag,window)
    #
    #	Implementation:
    #
    #	cum(k,l) = sum_{n=0}^{N-1} conj(signal(n))*signal(n+k)*signal(n+l)/N
    #
    #	k,l = {-maxlag,...,-1,0,1,...,maxlag}, n = {0,1,...,N-1}
    #
    #	bisp=fftshift(fft2(ifftshift(cum.*wind)))
    #
    #	Example:
    #
    #	» [b,f,c,l]=bisp3cum([1-i -1+i],1,1)
    #
    #	b =
    #
    #	  -5.1962 - 5.1962i        0            -0.0000 - 0.0000i
    #	        0                  0                  0          
    #	  -0.0000 - 0.0000i   0.0000 + 0.0000i   5.1962 + 5.1962i
    #
    #	f =
    #
    #	   -0.5000         0    0.5000
    #
    #	c =
    #
    #	  -1.0000 + 1.0000i   1.0000 - 1.0000i        0          
    #	   1.0000 - 1.0000i        0            -1.0000 + 1.0000i
    #	        0            -1.0000 + 1.0000i   1.0000 - 1.0000i
    #
    #	l =
    #
    #	    -1     0     1
    #
    #	References:
    #
    #	C. L. Nikias, A. P. Petropulu, Higher-Order Spectra Analysis:  A Nonlinear Signal
    #	Processing Framework, PTR Prentice Hall, Englewood Cliffs, NJ, 1993.
    #
    #	T. S. Rao, M. M. Gabr, An Introduction to Bispectral Analysis and Bilinear Time
    #	Series Models, Lecture Notes in Statistics, Volume 24, D. Brillinger, S. Fienberg,
    #	J. Gani, J. Hartigan, K. Krickeberg, Editors, Springer-Verlag, New York, NY, 1984.
    #
    #	Copyright (c) 2000
    #	Tom McMurray
    #	mcmurray@teamcmi.com
    
    #	assign default input parameters
    
    #	while signal is unsupported, enter supported signal or return for 0 outputs
    sample, record = signal.shape
    
    #	if signal is a row vector, modify to a column vector
    
    if sample == 1:    
        sample = record    
        record = 1    
        signal = signal.reshape()    
    
    #	while samprate is unsupported, enter supported samprate or return for samprate=1
    
#    while isempty(samprate):    
#        samprate = input(mcat([mstring('signal sample rate is empty:\\nenter finite positive scalar or '), mstring('return for signal sample rate = 1\\n')]))    
#        if isempty(samprate):        
#            samprate = 1        
#    while samprate <= 0 | not isnumeric(samprate) | not isfinite(samprate) | length(samprate) != 1:    
#        samprate = input(mcat([mstring('signal sample rate = '), num2str(samprate(mslice[:]).T), mstring(' <= 0, \'nonnumeric, nonfinite, or nonscalar:\\nenter finite positive scalar or '), mstring('return for signal sample rate = 1\\n')]))    
#        if isempty(samprate):        
#            samprate = 1        
    sample1 = sample - 1
    strsample1 = str(sample1)
    
    #	while maxlag is unsupported, enter supported maxlag or return for maxlag=0
    
#    while isempty(maxlag):    
#        maxlag = input(mcat([mstring('maximum lag is empty:\\nenter integer scalar >= 0, <= signal '), mstring('sample length - 1 = '), strsample1, mstring(', or return for maximum lag = 0\\n')]))    
#        if isempty(maxlag):        
#            maxlag = 0        
#    while maxlag < 0 | maxlag > sample1 | rem(maxlag, 1) | not isnumeric(maxlag) | not isfinite(maxlag) | length(maxlag) != 1:    
#        maxlag = input(mcat([mstring('maximum lag = '), num2str(maxlag(mslice[:]).T), mstring(' < 0, > signal sample \'length - 1 = '), strsample1, mstring(', noninteger, nonnumeric, nonfinite, or \'nonscalar:\\nenter integer scalar >= 0, <= '), strsample1, mstring(', or return for '), mstring('maximum lag = 0\\n')]))    
#        if isempty(maxlag):        
#            maxlag = 0        
    
    #	compute lag vector
    
    lagindex = range(-maxlag,maxlag)
    lag = lagindex / samprate
    
    #	if maxlag, compute freq vector
    
    if maxlag:    
        freq = lagindex / maxlag / 2 * samprate    
        
        #	else, freq=0 and specify no window/biased estimate computation
        
    else:    
        freq = 0    
        window = 'n'    
        scale = 'b'    
    
    #	resolve window
    
    window = str(window)
    windowarr=('none', 'uniform', 'sasaki', 'priestley', 'parzen', 'hamming', 'gaussian', 'daniell')
    if not window in windowarr:
        print "error"
    
    #	while window is unsupported, enter supported window or return for window='n'
    
#    while isempty(windowind) | isempty(window):    
#        window = lower(input(mcat([mstring('window = '), window(mslice[:]).T, mstring(' unresolved:\\nenter none, \'uniform, sasaki, priestley, parzen, hamming, gaussian, daniell, or '), mstring('return for window = none\\n')]), mstring('s')))    
#        if isempty(window):        
#            window = mstring('n')        
#        windowind = strmatch(window, windowarr)    
    
    #	if window is unique, assign supported window
    
#    if len(windowind) == 1:    
#        window = windowarr(windowind)    
        
        #	else window=='p', window='priestley'
        
    else:    
        window = mstring('priestley')    
    
    #	generate constants
    
    maxlag1 = maxlag + 1
    maxlag2 = maxlag * 2
    maxlag21 = maxlag2 + 1
    samp1ind = range(sample, 1, -1)
    samlsamind = range(sample - maxlag:sample)
    ml1samind = mslice[maxlag1:sample]
    ml211ind = mslice[maxlag21:-1:1]
    zeros1maxlag = zeros(1, maxlag)
    zerosmaxlag1 = zeros1maxlag(mslice[:])
    onesmaxlag211 = ones(maxlag21, 1)
    strmaxlag21 = num2str(maxlag21)
    
    #	subtract mean from signal
    
    meansig = mean(signal)
    signal = signal - meansig(ones(sample, 1), mslice[:])
    
    #	initialize cumulant matrix
    
    cum = zeros(maxlag21)
    
    #	signal record cumulant computation loop
    
    tic
    for k in mslice[1:record]:    
        time = cputime    
        sig = signal(mslice[:], k)    
        trflsig = sig(samp1ind).cT    
        toepsig = toep(mcat([sig(samlsamind), OMPCSEMI, zerosmaxlag1]), mcat([conj(trflsig(ml1samind)), zeros1maxlag]))    
        
        #	compute cumulant
        
        cum = cum + toepsig *elmul* trflsig(onesmaxlag211, mslice[:]) * toepsig.T    
        disp(mcat([mstring('record '), num2str(k), mstring(':  time = '), num2str(cputime - time), mstring(' seconds')]))    
    cum = cum / record
    clear(mstring('samp1ind'), mstring('samlsamind'), mstring('ml1samind'), mstring('zerosmaxlag1'), mstring('sig'), mstring('trflsig'), mstring('toepsig'))
    
    #	if scale=='b', compute biased cumulant
    
    if scale == mstring('b'):    
        cum = cum / sample    
        
        #	else, compute unbiased cumulant
        
    else:    
        scalmat = zeros(maxlag1)    
        for k in mslice[1:maxlag1]:        
            maxlag1k = maxlag1 - k        
            scalmat(k, mslice[k:maxlag1]).lvalue = repmat(sample - maxlag1k, 1, maxlag1k + 1)        
        end    
        scalmat = scalmat + triu(scalmat, 1).T    
        samplemaxlag1 = sample - maxlag1    
        maxlag1ind = mslice[maxlag:-1:1]    
        scalmat = mcat([scalmat, mcat([toep((mslice[samplemaxlag1:sample - 2]).T, mslice[samplemaxlag1:-1:sample - maxlag2]), OMPCSEMI, scalmat(maxlag1, maxlag1ind)])])    
        scalmat = mcat([scalmat, OMPCSEMI, scalmat(maxlag1ind, ml211ind)])    
        scalmat(scalmat < 1).lvalue = 1    
        cum = cum /eldiv/ scalmat    
        clear("scalmat")        
        maxlag1ind    
    time = num2str(toc)
    disp(mstring(' '))
    disp(mcat([strmaxlag21, mstring(' x '), strmaxlag21, mstring(' element cumulant computed in '), time, mstring(' seconds')]))
    
    #	generate lag window function
    
    if window(1) == mstring('n'):    
        wind = 1    
    else:    
        wind = lagwind(maxlag1, window)    
        
        #	generate 2d even window function
        
        windeven = mcat([wind(mslice[maxlag1:-1:2]), wind])    
        windeven = windeven(onesmaxlag211, mslice[:])    
        
        #	0 pad window function
        
        wind = mcat([wind, zeros1maxlag])    
        
        #	generate 2d window function
        
        wind = toep(wind(mslice[:]), mcat([wind(1), zeros(1, maxlag2)]))    
        wind = wind + tril(wind, -1).T    
        wind = wind(ml211ind, mslice[:]) *elmul* windeven *elmul* windeven.T    
        clear("windeven")    
    clear(mstring('ml211ind'), mstring('zeros1maxlag'), mstring('onesmaxlag211'))
    
    #	compute bispectrum
    
    tic
    bisp = fftshift(fft2(ifftshift(cum *elmul* wind)))
    time = num2str(toc)
    disp(mstring(' '))
    disp(mcat([strmaxlag21, mstring(' x '), strmaxlag21, mstring(' element bispectrum computed in '), time, mstring(' seconds')]))
    disp(mstring(' '))
    clear(mstring('wind'))
    
    #	plot mean signal
    
    meansig = mean(signal, 2)
    realsig = isreal(meansig)
    subplot(mstring('221'))
    if realsig:    
        plot((mslice[0:sample1]) / samprate, meansig)    
    else:    
        plot((mslice[0:sample1]) / samprate, abs(meansig))    
    fontsize = mstring('\\fontsize{8}')
    seconds = mstring('(\\its \\rm)')
    title(mcat([fontsize, mstring('Averaged Signal')]))
    xlabel(mcat([fontsize, mstring('Time '), seconds]))
    ylabel(mcat([fontsize, mstring('Signal (\\itV \\rm)')]))
    grid
    clear(mstring('meansig'))
    
    #	plot 3rd order cumulant
    
    subplot(mstring('222'))
    if realsig:    
        imagesc(lag, lag, cum)    
    else:    
        imagesc(lag, lag, abs(cum))    
    title(mcat([fontsize, mstring('3^{rd} Order Cumulant (\\itV \\rm^{3} )')]))
    xlabel(mcat([fontsize, mstring('Lag \\tau_{0} '), seconds]))
    ylabel(mcat([fontsize, mstring('Lag \\tau_{1} '), seconds]))
    axis(mstring('xy'))
    grid
    colorbar
    
    #	plot bispectrum
    
    subplot(mstring('223'))
    imagesc(freq, freq, abs(bisp))
    title(mcat([fontsize, mstring('Bispectrum Magnitude (\\itV \\rm^{3}/\\itHz \\rm^{2} )')]))
    hertz = mstring('(\\itHz \\rm)')
    fxlabel = mcat([fontsize, mstring('Frequency f_{0} '), hertz])
    xlabel(fxlabel)
    fylabel = mcat([fontsize, mstring('Frequency f_{1} '), hertz])
    ylabel(fylabel)
    axis(mstring('xy'))
    grid
    colorbar
    subplot(mstring('224'))
    imagesc(freq, freq, angle(bisp) * 180 / pi)
    title(mcat([fontsize, mstring('Bispectrum Phase (\\itdeg \\rm)')]))
    xlabel(fxlabel)
    ylabel(fylabel)
    axis(mstring('xy'))
    grid
    colorbar
    colormap(mstring('gray'))
