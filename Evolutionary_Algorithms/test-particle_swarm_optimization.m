addpath(genpath('.\2005'))

functions = [1 2 3 4 5 6 7 8 9 10]; % Functions being solved
%functions = [3 6 9];
numF = size(functions, 2);
nTimes = 20;                % Number of times in which a function is going to be solved
dimension = 30;             % Dimension of the problem

%* PSO parameters
populationSize = 100;
Vmax = 1.0;                 % min/max velocity
c_w = 1.5;                  % Cognitive weight
s_w = 0.5;                  % Social weight

for i = 1:numF
    
    fitfun = functions(i); % fitfun is the function that we are solving
    fprintf('\n-----  Function %d started  -----\n\n', fitfun);

    for t = 1:nTimes
        
        maxEval = 10000 * dimension; % maximum number of evaluation
        [value, upper, lower, objetiveValue, o, A, M, a, alpha, b] = getInformation_2005(fitfun, dimension);
        currentEval = 0;

        % Start generating the initial population
        population = zeros(populationSize, dimension);
        for j = 1:populationSize
            population(j,:) = lower + (upper-lower).*rand(1,dimension);
        end

        populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); % Fitness values of all individuals (smaller value is better)
        bestSolutionFitness = min(populationFitness);
        currentEval = currentEval + populationSize;
        
        fprintf('>> %dth run, Initial best individual fitness: %d\n', t, bestSolutionFitness); % Temp
        
        % Initialize particles
        V = -Vmax + (Vmax + Vmax).*rand(populationSize, dimension); % Velocity for each particle
        pBest = population;                                         % Location of the best position found by each particle.
        pBest_fitness = populationFitness;                          % Fitness of the best solution found by each particle
        
        % Algorithm loop
        while(objetiveValue < bestSolutionFitness && currentEval < maxEval)
            
            % Update velocity
            [gFitness, gInd] = min(populationFitness);
            cognitive = c_w .* rand(populationSize, dimension) .* (pBest - population);
            social = s_w .* rand(populationSize, dimension) .* (population(gInd,:) - population);
            V = V + cognitive + social;
            V(V > Vmax) = Vmax;
            V(V < -Vmax) = -Vmax;
            
            % Update position
            population = population + V;

            populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b);
            bestSolutionFitness = min(populationFitness);
            currentEval = currentEval + populationSize;

            % Update best particles
            for j = 1:populationSize
                if populationFitness(j) < pBest_fitness(j)
                    pBest(j,:) = population(j,:);
                    pBest_fitness(j) = populationFitness(j);
                end
            end
            
        end

        % Best individual
        bestSolutionFitness = min(populationFitness);
        fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
        
    end
    
end
