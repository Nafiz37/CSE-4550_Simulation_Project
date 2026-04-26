export type DistributionType = 'Uniform' | 'Exponential' | 'Geometric' | 'Poisson' | 'Normal' | 'Binomial';

export const randomUniform = (): number => Math.random();

export const randomExponential = (lambda: number = 1): number => {
    return -Math.log(1 - Math.random()) / lambda;
};

export const randomGeometric = (p: number = 0.5): number => {
    return Math.floor(Math.log(Math.random()) / Math.log(1 - p));
};

export const randomPoisson = (lambda: number = 1): number => {
    let L = Math.exp(-lambda);
    let k = 0;
    let p = 1;
    do {
        k++;
        p *= Math.random();
    } while (p > L);
    return k - 1;
};

export const randomNormal = (mean: number = 0, stdDev: number = 1): number => {
    let u = 1 - Math.random();
    let v = Math.random();
    let z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    return z * stdDev + mean;
};

export const randomBinomial = (n: number = 10, p: number = 0.5): number => {
    let successes = 0;
    for (let i = 0; i < n; i++) {
        if (Math.random() < p) {
            successes++;
        }
    }
    return successes;
};

export const sampleEvent = (dist: DistributionType, baseProb: number): boolean => {
    // Generate a value and normalize it roughly to [0,1], then compare to baseProb
    let val = 0;
    switch (dist) {
        case 'Uniform':
            val = randomUniform();
            break;
        case 'Exponential':
            val = randomExponential(1) / 4; 
            break;
        case 'Geometric':
            val = randomGeometric(0.5) / 5;
            break;
        case 'Poisson':
            val = randomPoisson(1) / 4;
            break;
        case 'Normal':
            val = Math.abs(randomNormal(0, 1)) / 3;
            break;
        case 'Binomial':
            val = randomBinomial(10, 0.5) / 10;
            break;
    }
    return val < baseProb;
};

export const sampleRate = (dist: DistributionType, baseRate: number): number => {
    if (dist === 'Poisson') {
        return Math.max(0, randomPoisson(baseRate));
    }
    
    let multiplier = 1;
    switch (dist) {
        case 'Uniform':
            multiplier = randomUniform() * 2; 
            break;
        case 'Exponential':
            multiplier = randomExponential(1);
            break;
        case 'Geometric':
            multiplier = randomGeometric(0.5);
            break;
        case 'Normal':
            multiplier = Math.abs(randomNormal(1, 0.5));
            break;
        case 'Binomial':
            multiplier = randomBinomial(10, 0.5) / 5;
            break;
    }
    return Math.max(1, Math.round(baseRate * multiplier));
};
