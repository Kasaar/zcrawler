from urllib.parse import ParseResult
from os.path import dirname

class LinkHandler:
    def fixup_link(self, l : str, parsed_url : ParseResult) -> str:
            if (l is None or len(l) < 2):
                return None
                
            # Handle '/' links
            elif (len(l) > 1 and l[0] == '/' and l[0:2] != '//'):
                link_builder = [parsed_url.scheme, "://", parsed_url.hostname, l]
                ''.join(link_builder)
                return link_builder
                
            # Handle '//' links
            elif (len(l) > 1 and l[0:2] == '//'):
                link_builder = [parsed_url.scheme, ":", l]
                ''.join(link_builder)
                return link_builder
                
            # Handle './' links
            elif (len(l) > 1 and l[0:2] == './'):
                link_builder = [parsed_url.scheme, "://", parsed_url.hostname, dirname(parsed_url.path), l[1:]]
                ''.join(link_builder)
                return link_builder
                
            # Handle '#' links
            elif (l[0] == '#'):
                link_builder = [parsed_url.scheme, "://", parsed_url.hostname, parsed_url.path, l]
                ''.join(link_builder)
                return link_builder
                
            # Handle '../' links
            elif (len(l) > 3 and l[0:3] == '../'):
                link_builder = [parsed_url.scheme, "://", parsed_url.hostname, '/', l]
                ''.join(link_builder)
                return link_builder
                
            # Handle 'javascript:' links
            elif (len(l) > 11 and l[0:11] == 'javacript:'):
                return None
            
            # Handle 'mailto:' links
            elif (len(l) > 7 and l[0:7] == 'mailto:'):
                return None
            
            # Handle remaining links
            elif (len(l) > 5 and l[0:5] != 'https' and l[0:4] != 'http'):
                link_builder = [parsed_url.scheme, "://", parsed_url.hostname, l]
                ''.join(link_builder)
                return link_builder

    def in_domain(self, domain : str, parsed_url : ParseResult) -> bool:
        return 1 if domain == parsed_url.hostname else 0