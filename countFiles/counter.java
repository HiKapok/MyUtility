package prjCounter;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class counter {
	/** 文件后缀名黑名单，无白名单则使用黑名单 */
	private ArrayList<String> blackLists = new ArrayList<String>();
	/** 文件后缀名白名单，优先使用  */
	private ArrayList<String> whiteLists = new ArrayList<String>();
	/** 过滤某些目录 */
	private ArrayList<String> dirFilter = new ArrayList<String>();
	/** 分类型统计文件 */
	private HashMap<String,Integer> fileType = new HashMap<String,Integer>();
	/** 待处理文件列表 */
	private ArrayList<String> files = new ArrayList<String>();
	
	private long totalLinesAll = 0;
	private long blashLinesAll = 0;
	private long singleKuoAll = 0;
	private long singleZhuAll = 0;
	private long allSingleZhuAll =0;
	private long blockCommentLinesAll = 0;
	private long charCntAll = 0;
	private long noBlashCharCntAll = 0;
	private long singleStatementCntAll = 0;
	private long includeLineCntAll = 0; 
	
	private String prjRoot = "";
	
	private final String singleStatement="[^;\\s]+?;";
	private final String includeLine = "#.+?@@";
	private final String singleLineKuo="@@\\s*[\\{\\}]\\s*@@";
	private final String singleLineZhu = "@\\s*?/{2,}.+?@";
	private final String allSingleZhuShi = "/{2,}.+?@";
	private final String blockComments = "/\\*.+?\\*/";
	private final String notSingleZhu = "@[^@]*?//[^\"/@]*?\"[^\"/@]*?@";
	 
	private long getCounts(String reg,String str){
		long cnt = 0;
		Pattern pattern = Pattern.compile(reg);
		Matcher matcher = pattern.matcher(str);

		while(matcher.find()) {
	        ++cnt;
	    }
		
		return cnt;
	}
	/** 执行统计 */
	void runCount(){
		for(String filename:files){
			countEach(filename);
		}
	}
	
	private void countEach(String name){
		Pattern patternBlash = Pattern.compile("^\\s+$");
		Pattern patternBlockComment = Pattern.compile(blockComments);
		try {
			long totalLines = 0;
			long blashLines = 0;
			long singleKuo = 0;
			long singleZhu = 0;
			long allSingleZhu =0;
			long blockCommentLines = 0;
			long charCnt = 0;
			long noBlashCharCnt = 0;
			long singleStatementCnt = 0;
			long includeLineCnt = 0;
			StringBuffer sb = new StringBuffer();
			BufferedReader br = new BufferedReader(new FileReader(name));
			
			Stream<String> allContent = br.lines();
			
			Iterator<String> it = allContent.iterator();
			
			while(it.hasNext()){
				String tempString = it.next();									
				++totalLines;
				Matcher matcher = patternBlash.matcher(tempString);
				if(matcher.matches()||tempString.equals("")) ++blashLines;
				else tempString+="@@";
				sb.append(tempString);
			}
			singleKuo = getCounts(singleLineKuo,sb.toString());
			singleZhu = getCounts(singleLineZhu,sb.toString());
			singleStatementCnt = getCounts(singleStatement,sb.toString());
			includeLineCnt = getCounts(includeLine,sb.toString());
			allSingleZhu = getCounts(allSingleZhuShi,sb.toString())-getCounts(notSingleZhu,sb.toString());
			noBlashCharCnt = getCounts("\\S",sb.toString());
			charCnt = getCounts(".",sb.toString());
			Matcher matcherBlockComment = patternBlockComment.matcher(sb);

			while(matcherBlockComment.find()) {
				blockCommentLines+=getCounts("@@",matcherBlockComment.group())+1;
		    }
			
			allContent.close();
			br.close();		
			totalLinesAll+=totalLines;
			blashLinesAll+=blashLines;
			singleKuoAll+=singleKuo;
			singleZhuAll+=singleZhu;
			allSingleZhuAll+=allSingleZhu;
			blockCommentLinesAll+=blockCommentLines;
			charCntAll+=charCnt;
			noBlashCharCntAll+=noBlashCharCnt;
			singleStatementCntAll+=singleStatementCnt;
			includeLineCntAll+=includeLineCnt;
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		String nameExt=new String("");
		if(!name.contains(".")) nameExt="unknown";
		else nameExt = name.substring(name.lastIndexOf(".")+1);
		Integer count = fileType.get(nameExt); 
		if (count != null) {  
	    	fileType.put(nameExt, count + 1);  
	    } else {  
	    	fileType.put(nameExt, 1);  
	    }
	}
	/** 打印统计报告 */
	void printReport(){
		String [] temp = prjRoot.split("[\\\\/]+");
		System.out.println("工程:"+temp[temp.length-1]);

		for (String key : fileType.keySet()) {
			System.out.println(key+"类型文件总数:"+fileType.get(key));	
		}
		
		System.out.println("总行数:"+totalLinesAll);
		System.out.println("非空行数:"+(totalLinesAll-blashLinesAll));
		System.out.println("单括号行数:"+singleKuoAll);
		System.out.println("单行注释行数:"+singleZhuAll);
		System.out.println("所有单注释行数:"+allSingleZhuAll);
		System.out.println("多行注释行数:"+blockCommentLinesAll);
		System.out.println("总字符数:"+charCntAll);
		System.out.println("非空字符总数:"+noBlashCharCntAll);
		System.out.println("单语句总数:"+singleStatementCntAll);
		System.out.println("头文件包含总行数:"+includeLineCntAll);
		
	}
	/** 添加后缀名黑名单 */
	void addExtNameBlackList(String name){
		blackLists.add(name);
	}
	/** 添加目录名黑名单 */
	void addDirBlackLists(String name){
		dirFilter.add(name);
	}
	/** 添加后缀名白名单 */
	void addExtNameWhiteList(String name){
		whiteLists.add(name);
	}
	/** 设置工程目录路径 */
	void setPrjRoot(String name){
		File file = new File(name);	
		if(file.exists()) this.prjRoot = file.getAbsolutePath();
		else System.out.println("file \""+name+"\" doesn't exists.");
		this.getAllFiles();
	}
	/** 打印所有待处理文件 */
	void printAllFiles(){
		Iterator<String> it = files.iterator();
		while(it.hasNext()){
			System.out.println(it.next());
		}
	}
	
	private void getAllFiles(){
		Stack<String> dirBuff = new Stack<String>();
		dirBuff.push(prjRoot);
		while(!dirBuff.isEmpty()){
			String tempDir = dirBuff.pop();		
			File file = new File(tempDir); 		
			String[] fileLists = file.list();
			
			for(String tempName:fileLists){
				if(tempName.charAt(0)=='.') continue;
				
				String absoluteName = tempDir+file.separator+tempName;
				File tempFile = new File(absoluteName);
				if(tempFile.isDirectory()) { if(dirFilter.contains(tempName)) continue; dirBuff.push(tempFile.getAbsolutePath()); }
				else{
					String temp = tempFile.getAbsolutePath();
					if(!temp.contains(".")) continue;
					else temp=temp.substring(temp.lastIndexOf(".")+1);
					// 白名单为空则使用黑名单
					if(whiteLists.isEmpty()) { if(!blackLists.contains(temp)) this.files.add(absoluteName); }
					else if(whiteLists.contains(temp)) { this.files.add(absoluteName); }
				}
			}		
		}
	}
}
