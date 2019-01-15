#include <iostream>
#include <vector>
#include <stack>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <fstream>
#include <cstring>
#include <cstdlib>
#include <sstream>
#include <numeric>
#include <algorithm>
#include <thread>
#include <shared_mutex>
#include <mutex>
#include <queue>
#include <array>
#include <boost/container_hash/hash.hpp>

using namespace std;


string exec(const string cmd);
typedef struct state {
    int url;
    vector<int> intst;
    vector<int> avail_urls; 
    unordered_set<int> path;
    state(const int &u, const vector<int> &i, const vector<int> &a, const unordered_set<int> &p): 
        url(u), intst(i), avail_urls(a), path(p){
            path.insert(url);
        }
}state;

template<typename T>
struct vec_hash{
    const size_t operator()(const vector<T> &vec) const{
        return boost::hash_value(vec);
    }
};

int N = 0;
int finished = 0;
int NUM_THREADS = stoi(exec("nproc"));
queue<int> urlQ;

unordered_map<vector<int>, unordered_set<int>, struct vec_hash<int>> traversed_intersect;
vector<thread> threadPool;

mutex mq;
shared_mutex mutex_trintst;


string exec(const string cmd) {
    array<char, 128> buffer;
    string result;
    unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

vector<vector<int> > readIn(string filename){
    ifstream ifs;
    vector<vector<int> > rvec;
    int value;
    string line;
    ifs.open(filename);
    while (getline(ifs, line)){
        istringstream is(line);
        vector<int> cur_line;
        while(is >> value)
            cur_line.push_back(value);
        rvec.push_back(cur_line);
    }
    return rvec;
}

// REQUIREL vec1 and vec2 are sorted
vector<int> intersect(const vector<int> &vec1, const vector<int> &vec2){
    vector<int> intst;
    set_intersection(vec1.begin(), vec1.end(), vec2.begin(), vec2.end(), back_inserter(intst));
    return intst;
}

vector<vector<vector<int> > > everyPairIntst(const vector<vector<int> > &vec){
    unsigned size = vec.size();
    vector<vector<vector<int> > > pairIntst(size, vector<vector<int> >(size));
    for (int i = 0; i < size; i++){
        for (int j = i; j < size; j++){
            pairIntst[i][j] = intersect(vec[i], vec[j]);
            pairIntst[j][i] = pairIntst[i][j];
        }
    }
    return pairIntst;
}

vector<int> available_urls(const vector<vector<int> > &pairIntst, const vector<int> &poss_set, const int thisurl, const unordered_set<int> &path){
    vector<int> avail_urls;
    for (const int &url: poss_set){
        if (path.count(url) == 0  && url > thisurl && pairIntst[url].size() >= N)
            avail_urls.push_back(url);
    }
    return avail_urls;
}

bool inTraverse(const unordered_map<vector<int>, unordered_set<int>, struct vec_hash<int> > &traversed_intersect, const vector<int> &vec){
    mutex_trintst.lock_shared();
    if (traversed_intersect.count(vec) > 0){
        mutex_trintst.unlock_shared();
        return true;
    }
    mutex_trintst.unlock_shared();
    return false;
}

void threadFunc(const vector<int> &beref_gt_N, const vector<vector<vector<int> > > &pairIntst, const vector<vector<int> > &beref){
    int url;
    mq.lock();
    while(!urlQ.empty()){
        url = urlQ.front();
        urlQ.pop();
        cout << "begin: " << url << endl;
        mq.unlock();
        struct state first_state = {url, beref[url], available_urls(pairIntst[url], beref_gt_N, url, unordered_set<int>({url}) ), unordered_set<int>()};
        stack<state> dfs_stack;
        dfs_stack.push(first_state);
        while (!dfs_stack.empty()){
            state cur_state = dfs_stack.top();
            int &url = cur_state.url;
            vector<int> &intst = cur_state.intst;
            vector<int> &poss_set = cur_state.avail_urls;
            unordered_set<int> &path = cur_state.path;
            dfs_stack.pop();
            vector<int> avail_urls = available_urls(pairIntst[url], poss_set, url, path);
            if (avail_urls.empty() && path.size() > 1){
                mutex_trintst.lock();
                traversed_intersect[intst] = path;
                mutex_trintst.unlock();
                continue;
            }
            for (const int &next_url: avail_urls){
                vector<int> new_intst = intersect(intst, beref[next_url]);
                if (!inTraverse(traversed_intersect, new_intst) && new_intst.size() >= N)
                    dfs_stack.push(state(next_url, new_intst, avail_urls, cur_state.path));
            }
        }
        mq.lock();
        cout << "finished: " << ++finished << endl;
    }
    mq.unlock();
}

int main(int argc, char* argv[]){
    N = atoi(argv[1]);
    vector<vector<int> > beref = readIn(string(argv[2]));
    cout << string(argv[2]) << endl;
    vector<vector<vector<int> > > pairIntst = everyPairIntst(beref);
    vector<int> urls(beref.size());
    iota(urls.begin(), urls.end(), 0);

    vector<int> beref_gt_N;
    for (const int url: urls){
        if (beref[url].size() >= N){
            beref_gt_N.push_back(url);
            urlQ.push(url);
        }
    }
    for (int i = 0; i < NUM_THREADS; i++)
         threadPool.push_back(thread(threadFunc, beref_gt_N, pairIntst, beref));
    for (int i = 0; i < NUM_THREADS; i++)
        threadPool[i].join();
    for (const pair<vector<int>, unordered_set<int>> traversed_pair: traversed_intersect){
        vector<int> ordered_urls(traversed_pair.second.begin(), traversed_pair.second.end());
        sort(ordered_urls.begin(), ordered_urls.end());
        for (const int i: ordered_urls)
            cout << i << " ";
        cout << ": \n\t";
        for (const int i: traversed_pair.first)
            cout << i << " ";
        cout << endl << endl;
    }
    return 0;
}