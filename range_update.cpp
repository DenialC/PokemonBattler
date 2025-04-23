#include <iostream>
#include <vector>
using namespace std;

struct SegmentTree {
    int size;
    vector<long long> tree;

    void init(int n){
        size = 1;
        while (size < n) size *= 2;
        tree.assign(2 * size, 0);
    }

    void build(const vector<long long>& a, int x, int lx, int rx) {
        if (rx - lx == 1) {
            if (lx < (int)a.size()) {
                tree[x] = a[lx];
            }
            return;
        }
        int m = (lx + rx) / 2;
        build(a, 2 * x + 1, lx, m);
        build(a, 2 * x + 2, m, rx);
        tree[x] = tree[2 * x + 1] + tree[2 * x + 2];
    }

    void build(const vector<long long>& a) {
        build(a, 0, 0, size);
    }  

    void update(int i, long long v, int x, int lx, int rx) {
        if (rx - lx == 1) {
            tree[x] += v;
            return;
        }
        int m = (lx + rx) / 2;
        if (i < m) {
            update(i, v, 2 * x + 1, lx, m);
        } else {
            update(i, v, 2 * x + 2, m, rx);
        }
        tree[x] = tree[2 * x + 1] + tree[2 * x + 2];
    }

    void update(int i, long long v) {
        update(i, v, 0, 0, size);
    }

    long long query(int l, int r, int x, int lx, int rx) {
        if (l >= rx || r <= lx) return 0;
        if (l <= lx && rx <= r) return tree[x];
        int m = (lx + rx) / 2;
        long long left = query(l, r, 2 * x + 1, lx, m);
        long long right = query(l, r, 2 * x + 2, m, rx);
        return left + right;
    }
    long long query(int l, int r) {
        return query(l, r, 0, 0, size);
    }
};


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;

    vector<long long> arr(n);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }
    vector<long long> diff(n+1, 0);
    for (int i = 1; i < n; ++i) {
        diff[i] = arr[i] - arr[i-1];
    }
    SegmentTree st;
    st.init(n+1);
    st.build(diff);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int a, b;
            long long u;
            cin >> a >> b >> u;
            st.update(a-1, u);
            if (b < n) {
                st.update(b, -u);
            }
        } else {
            int k;
            cin >> k;
            cout << st.query(0, k) + arr[0] << endl;
        }

    }
    return 0;
}