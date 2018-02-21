class Video(object):
    def __init__(self, key):
        self.id = key
        self.size = float()
        self.connect_to = dict()
        self.sorted_ends = list()

    def sorting(self):
        self.sorted_ends = [(k, v) for v, k in sorted(
            [(v, k) for k, v in self.connect_to.items()], reverse=True
        )]

    def add_end_point(self, end_point, video_requests):
        self.connect_to[end_point] = video_requests

    def get_connections(self):
        return self.connect_to.keys()

    def get_id(self):
        return self.id

    def get_weight(self, end_point):
        return self.connect_to[end_point]

    def __lt__(self, other):
        return self.sorted_ends[0][1] < other.sorted_ends[0][1]


class EndPoint(object):
    def __init__(self, key):
        self.id = key
        self.dc_latency = int()
        self.connect_to_caches = dict()
        self.connect_to_videos = dict()
        self.sorted_caches = list()

    def add_cache(self, cache, c_latency):
        self.connect_to_caches[cache] = c_latency

    def add_video(self,video, v_requests):
        self.connect_to_videos[video]= v_requests

    def sorting(self):
        self.sorted_caches = [(k, v) for v, k in sorted(
            [(v, k) for k, v in self.connect_to_caches.items()]
        )]

    def __lt__(self, other):
        return self.sorted_caches[0][1] < other.sorted_ends[0][1]


class Cache(object):
    def __init__(self, key):
        self.id = key
        self.size = int()
        self.connect_to_ep = dict()

    def get_size(self):
        return self.size

    def add_end_point(self, end_point, weight):
        self.connect_to_ep[end_point] = weight

    def get_id(self):
        return self.id

    def get_connections(self):
        return self.connect_to_ep


class Streaming(object):
    def __init__(self):
        self.videos = dict()
        self.caches = dict()
        self.end_points = dict()
        self.videos_count = int()
        self.caches_count = int()
        self.end_points_count = int()

    def add_video(self, video_no):
        self.videos_count += 1
        new_video = Video(video_no)
        self.videos[video_no] = new_video
        return new_video

    def add_cache(self, cache_no):
        self.caches_count += 1
        new_cache = Cache(cache_no)
        self.caches[cache_no] = new_cache
        return new_cache

    def add_end_point(self, end_point_no):
        self.end_points_count += 1
        new_end_point = EndPoint(end_point_no)
        self.end_points[end_point_no] = new_end_point
        return new_end_point

    def add_link(self, kind, frm, to, weight):
        if kind == 've':
            if frm not in self.videos:
                self.add_video(frm)
            if to not in self.end_points:
                self.add_end_point(to)
            self.videos[frm].add_end_point(self.end_points[to], weight)
            self.end_points[to].add_video(self.videos[frm], weight)
        elif kind == 'ec':
            if frm not in self.end_points:
                self.add_end_point(frm)
            if to not in self.caches:
                self.add_cache(to)
            self.end_points[frm].add_cache(self.caches[to], weight)
            self.caches[to].add_end_point(self.end_points[frm], weight)


def main():
    numbVideo, numbEndPoint, numbRequest, numbCaches, cachesCap, videoSizes, latencyCaches, latencyDataCenter, request = enum(
        "me_at_the_zoo.in")

    stream = Streaming()
    for video in range(numbVideo):
        new_video = stream.add_video(video)
        new_video.size = videoSizes[video]

    for cache in range(numbCaches):
        new_cache = stream.add_cache(cache)
        new_cache.size = cachesCap

    for end_point in range(numbEndPoint):
        new_end_point = stream.add_end_point(end_point)
        new_end_point.dc_latency = latencyDataCenter[end_point]

    for k, v in latencyCaches.items():
        stream.add_link('ec', int(k[0]), int(k[2]), v)

    for requests, video, end_point in request:
        stream.add_link('ve', video, end_point, requests)

    print(stream.caches[0].get_connections().values())

    print(s)





def enum(filename):
    """
    argument: file name
    returns:
        numbVideo:
        numbEndPoint
        numbRequest
        numbCaches
        cachesCap
        videoSizes:list it's index represent the video and items are the sizes of videos
        latencyCaches: dictionary-->key: is  endpoints (int) / value:datacenter latency of the endpoint
        latencyDataCenter:dictionary-->key: is endpoint-cache number(str) / value:The latency the specified endpoint to the specified cache
        request:list of tuple---> (number of requests,video number,endPoint)
    """
    fh = open(filename, "r")

    videoSizes = list()
    latencyCaches = dict()
    latencyDataCenter = dict()
    request = list()

    numbVideo, numbEndPoint, numbRequest, numbCaches, cachesCap = map(int, fh.readline().strip().split())

    videoSizes = list(map(int, fh.readline().strip().split()))

    for endPoint in range(numbEndPoint):
        datacenter_latency, numbConnectedCaches = map(int, fh.readline().strip().split())
        latencyDataCenter[endPoint] = int(datacenter_latency)

        for cache in range(numbConnectedCaches):
            latencyCaches[str(endPoint) + "-" + str(cache)] = int(fh.readline().strip().split()[1])
    for req in range(numbRequest):
        video, endPoint, requests = map(int, fh.readline().strip().split())
        request.append((requests, video, endPoint))
    fh.close()

    return numbVideo, numbEndPoint, numbRequest, numbCaches, cachesCap, videoSizes, latencyCaches, latencyDataCenter, request





if __name__ == '__main__':
    print('Starting...')
    main()
    print('\nEnd...')