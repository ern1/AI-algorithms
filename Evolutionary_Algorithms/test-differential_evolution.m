addpath(genpath('.\2005'))

functions = [1 2 3 4 5 6 7 8 9 10]; % Functions being solved
%functions = [3 6 9];
numF = size(functions, 2);
nTimes = 20;                % Number of times in which a function is going to be solved
dimension = 30;             % Dimension of the problem

% DE parameters
populationSize = 100;
F = 0.5;                    % Scaling factor, interval [0, 2]
pRecombination = 0.8;       % Recombination probabiltiy

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
            population(j,:) = lower + (upper - lower).*rand(1,dimension);
        end

        populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
        bestSolutionFitness = min(populationFitness);
        currentEval = currentEval + populationSize;
        
        fprintf('>> %dth run, Initial best individual fitness: %d\n', t, bestSolutionFitness); % Temp

        % Algorithm loop
        while(objetiveValue < bestSolutionFitness && currentEval < maxEval)
            
            % Mutate the population to obtain mutated population
            mutatedPopulation = zeros(populationSize, dimension);
            for j = 1:populationSize
                r = randperm(populationSize, 3); 
                %r = randi(populationSize, 3, 1);
                mutatedPopulation(j,:) = population(r(1),:) + F * (population(r(2),:) - population(r(3),:));
            end

            % Recombine each mutated individual with its parent to get offspring
            offspring = zeros(populationSize, dimension);
            trial = zeros(1, dimension);
            for j = 1:populationSize
                krand = randi(dimension); 
                for k = 1:dimension
                    if pRecombination > rand() || k == krand
                        trial(k) = mutatedPopulation(j,k);
                    else
                        trial(k) = population(j,k);
                    end
                end
                offspring(j,:) = trial;
            end
            
            % Actualize population with the set of new offspring (selection)
            offspringFitness = calculateFitnessPopulation_2005(fitfun, offspring, o, A, M, a, alpha, b);
            for j = 1:populationSize
                if offspringFitness(j) < populationFitness(j)
                    population(j,:) = offspring(j,:);
                end
            end

            populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b);
            bestSolutionFitness = min(populationFitness);
            currentEval = currentEval + populationSize;

        end

        % Best individual
        bestSolutionFitness = min(populationFitness);
        fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
                
    end
    
end
