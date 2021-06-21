package net.redborder.utils.types.impl;

import net.redborder.utils.types.Type;

import com.google.gson.Gson;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class QuestionnaireType implements Type {
    private Integer id = 1;
    private String name = "";
    private Integer questionCounter = -1;
    private Integer clientCounter = 0;
    private Integer answerCounter = 0;
    private List<Object> questions;
    private List<Object> answers;
    private List<Object> clients;
    private Random randomGen = new Random();
    
    private Integer multipleCounter = 1;
    private Boolean multiple = false;
    private ArrayList<Integer> multiplePrevious = new ArrayList<Integer>();

    public QuestionnaireType(Map<String, Object> params) {
        this.id = (Integer) params.get("id");
        this.name = (String) params.get("name");
        this.questions = (List<Object>) params.get("questions");
        this.clients = (List<Object>) params.get("clients");
        this.clientCounter = randomGen.nextInt(clients.size());
    }

    public void reset() {
        questionCounter = 0;
        clientCounter = randomGen.nextInt(clients.size());
    }
    
    @Override
    public Object get() {

        questionCounter++;
        if ( questionCounter >= questions.size()) {
            questionCounter = 0;
            clientCounter = randomGen.nextInt(clients.size());
        }

        Map<String, Object> coordinates = new HashMap<>();

        coordinates.put("questionnaire_id", id);
        coordinates.put("questionnaire_name", name);

        Map<String, Object> questionInfo = (Map<String, Object>) questions.get(questionCounter);
        coordinates.put("question_id", questionInfo.get("id"));
        coordinates.put("question", questionInfo.get("value"));

        Map<String, Object> answerInfo = (Map<String, Object>) questionInfo.get("answers");
        String type = (String) answerInfo.get("type");
        List<String> answerList = (List<String>) answerInfo.get("values");
        
        if (type.equals("multiple"))  {
            multipleCounter--;

            if (!multiple) {
                multiple = true;
                multipleCounter = randomGen.nextInt(answerList.size());
            }

            if (multipleCounter > 1)
                questionCounter--;
            else {
                multiple = false;
                multipleCounter = 1;
                multiplePrevious.clear();
            }
        }

        Integer rand = randomGen.nextInt(answerList.size());
        if (multiple) {
            while(multiplePrevious.contains(rand)) rand = randomGen.nextInt(answerList.size());
            multiplePrevious.add(rand);
        }

        coordinates.put("answer", answerList.get(rand));
        coordinates.put("answer_id", answerCounter);
        answerCounter++;

        Map<String, Object> clientInfo = (Map<String, Object>) clients.get(clientCounter);
        for (String client : clientInfo.keySet()) {
            coordinates.put(client, clientInfo.get(client));
        }

        return coordinates;

    }
}
